"""
ASGI config for myportfolio project.

This file contains the ASGI configuration required to serve up your
web application asynchronously. It exposes the ASGI callable as a module-level
variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'django' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myportfolio.settings')

# Get the ASGI application for the Django project
application = get_asgi_application()
