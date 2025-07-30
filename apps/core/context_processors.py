# Create this file: apps/core/context_processors.py

from apps.products.models import Category

def global_context(request):
    """
    Add global context variables available to all templates
    """
    return {
        'global_categories': Category.objects.filter(is_active=True)[:6],  # Limit for navbar
        'all_categories': Category.objects.filter(is_active=True),
        'featured_categories': Category.objects.filter(is_active=True, parent__isnull=True)[:4],  # Top-level categories
    }