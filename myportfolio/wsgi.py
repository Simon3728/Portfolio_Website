"""
WSGI config for myportfolio project.

This file contains the WSGI configuration required to serve up your
web application at deployment. It exposes the WSGI callable as a module-level
variable named `application`.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

# Set the default settings module for the 'django' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')

# Get the WSGI application for the Django project
application = get_wsgi_application()
