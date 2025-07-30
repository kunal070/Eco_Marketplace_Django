from django.urls import path
from .views import UserDashboardView, SearchHistoryView, PopularProductsView, AnalyticsDashboardView
from . import views

app_name = 'analytics'
urlpatterns = [
    path('dashboard/', AnalyticsDashboardView.as_view(), name='dashboard'),
    path('history/', SearchHistoryView.as_view(), name='user_history'),
    path('popular/', PopularProductsView.as_view(), name='popular_products'),
    #path('analytics/', views.analytics_dashboard, name='analytics_dashboard'),
]
