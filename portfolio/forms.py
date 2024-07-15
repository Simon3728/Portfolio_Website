"""
Forms for the portfolio app.
"""

from django import forms

class ContactForm(forms.Form):
    """
    A form for users to contact the site owner.
    """
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control text-black'})
    )  # Text input field for the user's name with Bootstrap styling.

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control text-black'})
    )  # Email input field for the user's email with Bootstrap styling.

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control text-black'})
    )  # Text input field for the subject of the message with Bootstrap styling.

    message = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control text-black'})
    )  # Text area for the user's message with Bootstrap styling.
