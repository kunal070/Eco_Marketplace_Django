import time
from .models import VisitLog
from django.utils.timezone import now
from .models import SiteAnalytics

class VisitTrackingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        today = now().date()

        analytics, created = SiteAnalytics.objects.get_or_create(date=today)

        if not request.session.get('visited_today', False):
            analytics.visits += 1
            analytics.save()
            request.session['visited_today'] = True

        return self.get_response(request)
