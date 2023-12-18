from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, ProfileForm
from .models import Profile

class SignUpView(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'accounts/signup.html'

def view_profile(request):
    # Assumes that the profile is always created upon user creation
    # You might need to handle the case where the profile does not exist using get_or_create
    return render(request, 'accounts/view_profile.html', {'user': request.user})

def edit_profile(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)  # This will create a profile if one does not exist
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)  # Use the profile instance we just got or created
        if form.is_valid():
            form.save()
            return redirect('view_profile')  # Replace 'profile' with the actual name of the URL pattern for viewing the profile
    else:
        form = ProfileForm(instance=profile)  # Use the profile instance we just got or created
    return render(request, 'accounts/edit_profile.html', {'form': form})




