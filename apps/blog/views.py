from django.views.generic import ListView, DetailView, TemplateView
from .models import BlogPost, GreenTip, FAQ

class BlogListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_list.html'
    context_object_name = 'posts'

class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'

class GreenTipsView(ListView):
    model = GreenTip
    template_name = 'blog/green_tips.html'
    context_object_name = 'tips'

class FAQView(ListView):
    model = FAQ
    template_name = 'blog/faq.html'
    context_object_name = 'faqs'
