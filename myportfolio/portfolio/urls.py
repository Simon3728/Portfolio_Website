from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('resume/', views.resume, name='resume'),
    path('contact/', views.contact, name='contact'),
    path('privacy/', views.privacy, name='privacy'),
    path('terms/', views.terms, name='terms'),
    # Project Links
    path('projects/', views.projects, name='projects'),
    path('projects/gda_calculator/', views.gda_calculator, name='gda_calculator'),
    path('projects/sspp_solver/', views.sspp_solver, name='sspp_solver'),
]
