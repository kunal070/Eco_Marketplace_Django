from django.views.generic import TemplateView, ListView
from .models import VisitLog, SearchHistory, PopularProduct
from django.contrib.auth.mixins import LoginRequiredMixin

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

class AnalyticsView(LoginRequiredMixin, ListView):
    model = VisitLog
    template_name = 'analytics/analytics.html'
    context_object_name = 'visits'

    def get_queryset(self):
        return VisitLog.objects.filter(user=self.request.user).order_by('-timestamp')

class SearchHistoryView(LoginRequiredMixin, ListView):
    model = SearchHistory
    template_name = 'analytics/user_history.html'
    context_object_name = 'searches'

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user).order_by('-timestamp')

class PopularProductsView(LoginRequiredMixin, ListView):
    model = PopularProduct
    template_name = 'analytics/popular_products.html'
    context_object_name = 'popular_products'

    def get_queryset(self):
        return PopularProduct.objects.order_by('-views')[:10]
