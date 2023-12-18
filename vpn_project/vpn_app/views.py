from django.shortcuts import render, redirect
from .models import VpnServer, ConnectionLog
from .forms import VpnServerForm, ConnectionLogForm
from django.core.paginator import Paginator
import requests
from django.db.models import Count, Sum
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import logging

logger = logging.getLogger(__name__)


# View for the home page
def home(request):
    return render(request, 'vpn_app/home.html')


# View for listing VPN servers
def server_list(request):
    servers = VpnServer.objects.all()
    return render(request, 'vpn_app/server_list.html', {'servers': servers})


# View for adding a new VPN server
def add_vpn_server(request):
    if request.method == 'POST':
        form = VpnServerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('server_list')
    else:
        form = VpnServerForm()
    return render(request, 'vpn_app/add_vpn_server.html', {'form': form})


# View for connection logs
def connection_logs(request):
    logs = ConnectionLog.objects.all()
    paginator = Paginator(logs, 10)  # Show 10 logs per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'vpn_app/connection_logs.html', {'page_obj': page_obj})


# View for adding a new connection log
def add_connection_log(request):
    if request.method == 'POST':
        form = ConnectionLogForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('connection_logs')
    else:
        form = ConnectionLogForm()
    return render(request, 'vpn_app/add_connection_log.html', {'form': form})


# View for editing an existing VPN server
def edit_vpn_server(request, pk):
    server = VpnServer.objects.get(pk=pk)
    if request.method == 'POST':
        form = VpnServerForm(request.POST, instance=server)
        if form.is_valid():
            form.save()
            return redirect('server_list')
    else:
        form = VpnServerForm(instance=server)
    return render(request, 'vpn_app/edit_vpn_server.html', {'form': form})


# View for editing an existing connection log
def edit_connection_log(request, pk):
    log = ConnectionLog.objects.get(pk=pk)
    if request.method == 'POST':
        form = ConnectionLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('connection_logs')
    else:
        form = ConnectionLogForm(instance=log)
    return render(request, 'vpn_app/edit_connection_log.html', {'form': form})


@login_required
def show_proxy_page(request):
    return render(request, 'vpn_app/proxy_page.html')


@login_required
def proxy_view(request):
    context = {
        'error_message': None,
        'website_content': None,
    }

    user_input_url = request.GET.get('site_url')
    if not user_input_url:
        context['error_message'] = 'No URL provided'
        return render(request, 'vpn_app/proxy_page.html', context)

    # Validate the URL
    parsed_url = urlparse(user_input_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        context['error_message'] = 'Invalid URL provided'
        return render(request, 'vpn_app/proxy_page.html', context)

    if parsed_url.scheme not in ['http', 'https']:
        context['error_message'] = 'URL must start with http:// or https://'
        return render(request, 'vpn_app/proxy_page.html', context)

    try:
        # Make the request to the external URL
        response = requests.get(user_input_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Attempt to get the first VpnServer instance
            vpn_server_instance = VpnServer.objects.first()
            if not vpn_server_instance:
                context['error_message'] = 'VPN server instance not found.'
                return render(request, 'vpn_app/proxy_page.html', context)

            # Log the connection in the database
            log_entry = ConnectionLog.objects.create(
                user=request.user,
                vpn_server=vpn_server_instance,
                external_url=user_input_url,
                site_visited=parsed_url.netloc,
                data_transferred=len(response.content)  # Assuming the response.content is not streamed
            )

            # Use BeautifulSoup to parse the HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Rewrite all the URLs so they point back to the proxy view
            for tag in soup.find_all(['a', 'form', 'link', 'script', 'img']):
                # Rewrite 'href' attributes for anchor tags
                if tag.name == 'a' and tag.has_attr('href'):
                    tag['href'] = urljoin(user_input_url, tag['href'])
                    tag['href'] = f'/proxy-view/?site_url={quote(tag["href"])}'
                # Rewrite 'action' attributes for form tags
                elif tag.name == 'form' and tag.has_attr('action'):
                    tag['action'] = urljoin(user_input_url, tag['action'])
                    tag['action'] = f'/proxy-view/?site_url={quote(tag["action"])}'
                # Rewrite 'src' attributes for image, script, and link tags
                elif tag.name in ['link', 'script', 'img'] and tag.has_attr('src'):
                    tag['src'] = urljoin(user_input_url, tag['src'])
                    tag['src'] = f'/proxy-view/?site_url={quote(tag["src"])}'

            context['website_content'] = str(soup)
        else:
            # Handle responses other than 200 OK
            context['error_message'] = f'Failed to retrieve website, status code: {response.status_code}'

    except requests.RequestException as e:
        # Handle any requests-related exceptions
        context['error_message'] = f'An error occurred: {str(e)}'

    return render(request, 'vpn_app/proxy_page.html', context)


@login_required
def statistics_view(request):
    user_stats = (ConnectionLog.objects
                  .filter(user=request.user)
                  .values('site_visited')
                  .annotate(Count('id'), Sum('data_transferred'))
                  .order_by('site_visited'))
    context = {
        'user_stats': user_stats,
    }
    return render(request, 'vpn_app/statistics.html', context)
