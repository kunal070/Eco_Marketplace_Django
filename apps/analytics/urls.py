from django.urls import path
from .views import UserDashboardView, SearchHistoryView, PopularProductsView
app_name = 'analytics'
urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('history/', SearchHistoryView.as_view(), name='user_history'),
    path('popular/', PopularProductsView.as_view(), name='popular_products'),
]
