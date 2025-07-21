from django.urls import path
from .views import (
    UserDashboardView,
    AnalyticsView,
    SearchHistoryView,
    PopularProductsView,
)
from . import views
app_name = 'analytics'

urlpatterns = [
    path('dashboard/', UserDashboardView.as_view(), name='dashboard'),
    path('visits/', AnalyticsView.as_view(), name='visits'),
    path('', views.AnalyticsView.as_view(), name='overview'),
    path('search-history/', SearchHistoryView.as_view(), name='search_history'),
    path('popular-products/', PopularProductsView.as_view(), name='popular_products'),
]
