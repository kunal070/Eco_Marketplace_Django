from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # App URLs - Will be uncommented as we create each app's URLs
    path('', include('apps.core.urls')),                    # Homepage, about, contact
    path('auth/', include('apps.authentication.urls')),     # Login, register, profile
    # path('products/', include('apps.products.urls')),       # Products, categories, search
    # path('messages/', include('apps.messaging.urls')),      # User messaging
    # path('reviews/', include('apps.reviews.urls')),         # Reviews and ratings
    # path('analytics/', include('apps.analytics.urls')),     # User history, dashboard
    path('analytics/', include('apps.analytics.urls', namespace='analytics')),
    path('blog/', include('apps.blog.urls')), # Blog posts, green tips
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug Toolbar URLs (only in development)
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns