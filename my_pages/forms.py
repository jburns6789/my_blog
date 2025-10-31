from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'What would you like to discuss?',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 6, 
                'placeholder': 'Tell me about your project or inquiry...',
                'required': True
            }),
        }