from django.views.generic import ListView, DetailView, TemplateView
from .models import BlogPost, GreenTip, FAQ
from django.shortcuts import render

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
