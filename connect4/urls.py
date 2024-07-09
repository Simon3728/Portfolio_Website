from django.urls import path
from . import views

urlpatterns = [
    path('projects/connect4/', views.connect4, name='connect4'),
]