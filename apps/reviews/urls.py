from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    # Review listing and details
    path('product/<int:product_id>/', views.ReviewListView.as_view(), name='review_list'),
    path('detail/<int:pk>/', views.review_detail, name='review_detail'),
    
    # Create and edit reviews
    path('product/<int:product_id>/add/', views.ReviewCreateView.as_view(), name='add_review'),
    path('edit/<int:pk>/', views.ReviewUpdateView.as_view(), name='edit_review'),
    path('delete/<int:pk>/', views.delete_review, name='delete_review'),
    
    # User reviews
    path('my-reviews/', views.UserReviewsView.as_view(), name='user_reviews'),
    
    # AJAX endpoints
    path('toggle-helpful/', views.toggle_helpful, name='toggle_helpful'),
    
    # Reporting
    path('report/<int:review_id>/', views.report_review, name='report_review'),
]