from django.urls import path
from .views import BlogListView, BlogDetailView, GreenTipsView, FAQView
from . import views
from .views import FAQView
from .views import BlogListView, BlogDetailView, GreenTipsView, FAQView, subscribe_newsletter

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    # path('tips/', GreenTipsView.as_view(), name='green_tips'),
    path('green-tips/', views.GreenTipsView.as_view(), name='green_tips'),
    path('faq/', FAQView, name='faq'),
    # path('subscribe/', subscribe_newsletter, name='subscribe_newsletter'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),

]
