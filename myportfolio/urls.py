"""
URL configuration for myportfolio project.
"""
from django.urls import path, include

urlpatterns = [
    path('', include('portfolio.urls')),
    path('', include('us_election.urls')),
    path('', include('connect4.urls')),
]


