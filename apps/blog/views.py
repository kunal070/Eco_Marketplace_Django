from django.views.generic import ListView, DetailView, TemplateView
from .models import BlogPost, GreenTip, FAQ
from django.shortcuts import render, redirect
from .models import Newsletter
from django.contrib import messages
from django.http import JsonResponse
from django.db import IntegrityError

# Blog list view
class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    ordering = ['-created_at']


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog'


# Green Tips view
class GreenTipsView(ListView):
    model = GreenTip
    template_name = 'blog/green_tips.html'
    context_object_name = 'tips'
    ordering = ['-posted_on']



# FAQ view
def FAQView(request):
    faqs = FAQ.objects.all()
    return render(request, 'blog/faq.html', {'faqs': faqs})

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            if Newsletter.objects.filter(email=email).exists():
                messages.info(request, "You're already subscribed.")
            else:
                Newsletter.objects.create(email=email)
                messages.success(request, "Thank you for subscribing to our eco-newsletter!")
    return redirect(request.META.get('HTTP_REFERER', 'core:home'))
# def subscribe_newsletter(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         try:
#             Newsletter.objects.create(email=email)
#             messages.success(request, "Thank you for subscribing to our eco-newsletter!")
#         except IntegrityError:
#             messages.info(request, "You're already subscribed.")
#     return redirect(request.META.get('HTTP_REFERER', 'core:home'))