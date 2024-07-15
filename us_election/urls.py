"""
URL configuration for the us_election app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('projects/us_election/', views.us_election, name='us_election'),
]
