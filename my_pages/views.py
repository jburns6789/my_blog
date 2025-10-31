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
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
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
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST,
                    [settings.EMAIL_HOST_USER],
                    fail_silently=False,
                )
                messages.success(request, 'Thank you! Your message has been sent successfully.')
                return redirect('contact')
            except Exception as e:
                messages.error(request, 'Sorry, there was an error sending your message. Please try again.')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})
    

