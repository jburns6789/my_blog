from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

from .forms import ContactForm
from .models import Contact

class HomePageView(TemplateView):
    template_name = 'home.html'

class AboutPageView(TemplateView):
    template_name = 'about.html'

class SiteFeaturesView(TemplateView):
    template_name = 'sitefeatures.html'

from django.http import JsonResponse

def debug_view(request):
    return JsonResponse({"headers": dict(request.headers)}, status=200)

def contact_view(request):
    print(f"Contact view called - Method: {request.method}")
    if request.method == 'POST':
        print("Processing POST request")
        form = ContactForm(request.POST)
        
        print(f"Form data received: {request.POST}")  # Debug: show what data was submitted
        
        if form.is_valid():
            print("Form is valid, saving contact...")
            contact = form.save()

            subject = f"New Contact: {form.cleaned_data['subject']}"
            message = f"""
            Name: {form.cleaned_data['name']}
            Email: {form.cleaned_data['email']}
            Subject: {form.cleaned_data['subject']}

            Message:
            {form.cleaned_data['message']}
            """
            
            try:
                print("Attempting to send email...")
                print(f"FROM: {settings.DEFAULT_FROM_EMAIL}")
                print(f"TO: {getattr(settings, 'CONTACT_EMAIL', settings.DEFAULT_FROM_EMAIL)}")
                
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                print("Email sent successfully!")
                messages.success(request, 'Thank you! Your message has been sent successfully.')
                return redirect('contact')
            except Exception as e:
                print(f"Email sending failed: {str(e)}") 
                messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
        else:
            # ADD THIS DEBUGGING BLOCK
            print("Form validation FAILED!")
            print(f"Form errors: {form.errors}")
            print(f"Form non-field errors: {form.non_field_errors()}")
            for field, errors in form.errors.items():
                print(f"  {field}: {errors}")
            messages.error(request, 'Please correct the errors in the form.')
    else:
        print("Showing GET form")  # Add this for completeness
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
