from django.urls import path
from .views import BlogListView, BlogDetailView, GreenTipsView, FAQView

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
    path('tips/', GreenTipsView.as_view(), name='green_tips'),
    path('faq/', FAQView.as_view(), name='faq'),
]
