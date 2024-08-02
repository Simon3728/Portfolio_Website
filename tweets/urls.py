"""
URL configuration for the Tweets app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('projects/tweets/', views.tweets, name='tweets'),  # Map the 'tweets' URL to the tweets view
]
