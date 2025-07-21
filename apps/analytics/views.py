from django.views.generic import TemplateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import VisitLog, SearchHistory, PopularProduct

class UserDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'analytics/dashboard.html'

class SearchHistoryView(LoginRequiredMixin, ListView):
    model = SearchHistory
    template_name = 'analytics/user_history.html'
    context_object_name = 'searches'

    def get_queryset(self):
        return SearchHistory.objects.filter(user=self.request.user)

class PopularProductsView(TemplateView):
    template_name = 'analytics/popular_products.html'

    def get_context_data(self, **kwargs):
        from .models import PopularProduct
        context = super().get_context_data(**kwargs)
        context['popular_products'] = PopularProduct.objects.order_by('-views')[:5]
        return context
