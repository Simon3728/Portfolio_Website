"""
URL configuration for the Connect4 app.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('projects/connect4/', views.connect4, name='connect4'),  # Map the 'connect4' URL to the connect4 view
]
