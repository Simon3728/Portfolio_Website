"""
Views for the portfolio app.
"""

from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def home(request):
    """
    Render the home page.
    """
    return render(request, 'index.html')

def projects(request):
    """
    Render the projects page.
    """
    return render(request, 'projects.html')

def resume(request):
    """
    Render the resume page.
    """
    return render(request, 'resume.html')

def privacy(request):
    """
    Render the privacy policy page.
    """
    return render(request, 'privacy.html')

def terms(request):
    """
    Render the terms and conditions page.
    """
    return render(request, 'terms.html')

def gda_calculator(request):
    """
    Render the GDA calculator project page.
    """
    return render(request, 'projects/gda_calculator.html')

def sspp_solver(request):
    """
    Render the SSPP solver project page.
    """
    return render(request, 'projects/sspp_solver.html')

def contact(request):
    """
    Handle contact form submission.

    If the request method is POST, validate the form and send an email with the form data.
    Display a success message upon successful submission and redirect back to the contact page.
    If the request method is GET, display an empty contact form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            full_message = f"Message from {name} ({email}):\n\n{message}"

            # Send email
            send_mail(
                subject,
                full_message,
                email,
                ['simon-wellnhofer@gmx.de'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
