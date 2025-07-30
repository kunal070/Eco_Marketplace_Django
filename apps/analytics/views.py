from django.views import View
from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VisitLog, SearchHistory, PopularProduct
from django.shortcuts import render
from django.utils.timezone import now
from django.shortcuts import render
from .models import SiteAnalytics
from apps.products.models import Product
# from .models import Product  # or whatever your product model is
# from analytics.models import SearchHistory

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_products"] = PopularProduct.objects.order_by('-views')[:5]
        context["page_visits"] = VisitLog.objects.filter(user=self.request.user).order_by('-timestamp')[:5]
        return context

# class SearchHistoryView(LoginRequiredMixin, ListView):
#     model = SearchHistory
#     template_name = 'analytics/user_history.html'
#     context_object_name = 'searches'
#
#     def get_queryset(self):
#         return SearchHistory.objects.filter(user=self.request.user)
class SearchHistoryView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/user_history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['visit_logs'] = VisitLog.objects.filter(user=self.request.user).order_by('-timestamp')[:10]
        context['searches'] = SearchHistory.objects.filter(user=self.request.user).order_by('-timestamp')[:10]
        return context


class PopularProductsView(TemplateView):
    template_name = 'analytics/popular_products.html'

    def get_context_data(self, **kwargs):
        from .models import PopularProduct
        context = super().get_context_data(**kwargs)
        context['popular_products'] = PopularProduct.objects.order_by('-views')[:5]
        return context

class AnalyticsDashboardView(LoginRequiredMixin, TemplateView):
    template_name = "analytics/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["popular_products"] = PopularProduct.objects.order_by('-views')[:5]
        context["page_visits"] = VisitLog.objects.filter(user=self.request.user).order_by('-timestamp')[:5]

        stats = SiteAnalytics.objects.order_by('-date')[:7]
        context["stats"] = stats
        context["total_visits"] = sum(item.visits for item in stats)
        context["total_logins"] = sum(item.logins for item in stats)
        context['total_products'] = Product.objects.count()
        return context
