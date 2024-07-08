from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def home(request):
    return render(request, 'index.html')

def projects(request):
    return render(request, 'projects.html')

def resume(request):
    return render(request, 'resume.html')

def privacy(request):
    return render(request, 'privacy.html')

def terms(request):
    return render(request, 'terms.html')

def gda_calculator(request):
    return render(request, 'projects/gda_calculator.html')

def sspp_solver(request):
    return render(request, 'projects/sspp_solver.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email
            send_mail(
                subject,
                message,
                email,
                ['simon-wellnhofer@gmx.de'],
                fail_silently=False,
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})