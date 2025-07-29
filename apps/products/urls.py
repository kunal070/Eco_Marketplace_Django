from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    # Product listing and details
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Product management
    path('create/', views.ProductCreateView.as_view(), name='product_create'),
    path('edit/<int:pk>/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
    path('my-products/', views.MyProductsView.as_view(), name='my_products'),
    path('my-favorites/', views.MyFavoritesView.as_view(), name='my_favorites'),  # ADD THIS LINE

    # Category and search
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
    
    # AJAX endpoints
    path('<int:product_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:product_id>/mark-sold/', views.mark_as_sold, name='mark_as_sold'),
]