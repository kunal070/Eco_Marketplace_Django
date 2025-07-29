from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm


class HomeView(TemplateView):
    """
    Homepage view displaying featured products and categories
    """
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Eco-Friendly Marketplace'
        context['featured_message'] = 'Discover sustainable products for a greener future!'
        return context


class AboutView(TemplateView):
    """
    About page explaining our environmental mission
    """
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us - Our Green Mission'
        return context


class ContactView(TemplateView):
    """
    Contact page with form for user inquiries
    """
    template_name = 'contact.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Contact Us'
        context['form'] = ContactForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Send email (optional - configure email settings in Django settings)
            try:
                email_subject = f"Contact Form: {subject}"
                email_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"
                
                # Uncomment when email is configured
                # send_mail(
                #     email_subject,
                #     email_message,
                #     email,
                #     ['admin@ecomarket.com'],  # Replace with your admin email
                #     fail_silently=False,
                # )
                
                messages.success(request, 
                    f'Thank you, {name}! Your message has been sent successfully. '
                    'We will get back to you within 24 hours.')
                
                # Return a new form for another submission
                context = self.get_context_data(**kwargs)
                context['form'] = ContactForm()
                return render(request, self.template_name, context)
                
            except Exception as e:
                messages.error(request, 
                    'There was an error sending your message. Please try again later.')
        
        # If form is not valid, return with errors
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)