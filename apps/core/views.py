from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib import messages


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
        return context