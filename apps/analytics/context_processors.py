from .models import SiteAnalytics

def analytics_counts(request):
    stats = SiteAnalytics.objects.order_by('-date')[:7]
    total_visits = sum(item.visits for item in stats)
    total_logins = sum(item.logins for item in stats)

    return {
        'analytics_total_visits': total_visits,
        'analytics_total_logins': total_logins,
        
    }
