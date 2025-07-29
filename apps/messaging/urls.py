from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    # Main messaging views
    path('', views.InboxView.as_view(), name='inbox'),
    path('conversation/<int:pk>/', views.ConversationView.as_view(), name='conversation'),
    path('compose/', views.ComposeMessageView.as_view(), name='compose'),
    path('contact-seller/<int:product_id>/', views.ContactSellerView.as_view(), name='contact_seller'),
    path('contact-seller/', views.ContactSellerView.as_view(), name='contact_seller_general'),
    
    # AJAX and utility endpoints
    path('mark-as-read/', views.mark_as_read, name='mark_as_read'),
    path('delete/<int:pk>/', views.delete_conversation, name='delete_conversation'),
    path('search/', views.search_conversations, name='search'),
]