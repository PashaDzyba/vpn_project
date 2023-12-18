VPN Service Documentation
Overview
VPN Service is a web application that allows users to register and manage a virtual private network (VPN) through a simple web interface. Users can edit their personal details, view connection statistics, and create and manage their own sites using the app as a proxy server.

Getting Started:

Prerequisites

1. Docker

2. Git (for version control)

3. Python 3.9 or higher (if running locally without Docker)

Installation

Using Docker

1. Clone the repository: 
git clone https://github.com/your-username/vpn_project.git
cd vpn_project
2. Build the Docker image: docker-compose build
3. Start the Docker container: docker-compose up

Running Locally

1. Set up a virtual environment: python3 -m venv venv
source venv/bin/activate
2. Install the requirements: pip install -r requirements.txt
3. Run migrations to create database schema: python manage.py migrate
4. Start the development server: python manage.py runserver

Usage

Usage

Registering an Account

1. Navigate to <your-server-url>/register to create an account.
2. Fill in the required fields and submit the form to register.


Logging In

1. Go to <your-server-url>/login to access the login page.
2. Enter your credentials to log in.


Managing VPN Servers

1. View Servers: Navigate to the server list at <your-server-url>/servers.
2. Add Server: Click on 'Create Server' to add a new VPN server.
3. Edit Server: Click on the 'Edit' button next to a server to modify its details.

Viewing Connection Logs

1. Access <your-server-url>/logs to view a paginated list of connection logs.
2. Navigate between pages using the pagination controls at the bottom of the list.


Proxy Functionality

1. After logging in, you can create sites that act as proxies.
2. Navigate to <your-server-url>/proxy to add or manage your sites.
3. Click 'Go to Site' to navigate through the proxy.
