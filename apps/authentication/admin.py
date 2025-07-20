from django.contrib import admin
from .models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'location', 'phone_number', 'is_verified')
    search_fields = ('user__username', 'location', 'phone_number')
    list_filter = ('is_verified', 'location')
    ordering = ('user__username',)

admin.site.register(UserProfile, UserProfileAdmin)
