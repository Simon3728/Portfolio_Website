"""
Views for the tweets app.
"""

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages

def tweets(request):
    """
    Render the tweets page.
    """
    return render(request, 'projects/sentiment_analysis.html')