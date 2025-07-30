from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
from .models import SiteAnalytics

@receiver(user_logged_in)
def track_login(sender, request, user, **kwargs):
    today = now().date()
    analytics, created = SiteAnalytics.objects.get_or_create(date=today)
    analytics.logins += 1
    analytics.save()
