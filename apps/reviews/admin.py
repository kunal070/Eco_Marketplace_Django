from django.contrib import admin
from .models import Review, ReviewHelpful, ReviewReport, ProductRating


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['reviewer', 'product', 'rating', 'title', 'is_approved', 'is_verified_purchase', 'is_featured', 'created_at']
    list_filter = ['rating', 'is_approved', 'is_verified_purchase', 'is_featured', 'created_at']
    search_fields = ['title', 'content', 'reviewer__username', 'product__title']
    readonly_fields = ['created_at', 'updated_at', 'helpful_count']
    list_editable = ['is_approved', 'is_featured']
    
    fieldsets = (
        ('Review Information', {
            'fields': ('product', 'reviewer', 'rating', 'title', 'content')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_approved', 'is_verified_purchase', 'is_featured')
        }),
        ('Statistics', {
            'fields': ('helpful_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )


@admin.register(ReviewHelpful)
class ReviewHelpfulAdmin(admin.ModelAdmin):
    list_display = ['user', 'review', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'review__title']


@admin.register(ReviewReport)
class ReviewReportAdmin(admin.ModelAdmin):
    list_display = ['reporter', 'review', 'reason', 'is_resolved', 'created_at']
    list_filter = ['reason', 'is_resolved', 'created_at']
    search_fields = ['reporter__username', 'review__title', 'description']
    readonly_fields = ['created_at', 'resolved_at']
    list_editable = ['is_resolved']
    
    actions = ['mark_as_resolved']
    
    def mark_as_resolved(self, request, queryset):
        for report in queryset:
            if not report.is_resolved:
                report.resolve(request.user)
        self.message_user(request, f'{queryset.count()} reports marked as resolved.')
    mark_as_resolved.short_description = 'Mark selected reports as resolved'


@admin.register(ProductRating)
class ProductRatingAdmin(admin.ModelAdmin):
    list_display = ['product', 'average_rating', 'total_reviews', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['product__title']
    readonly_fields = ['average_rating', 'total_reviews', 'five_star_count', 'four_star_count', 
                      'three_star_count', 'two_star_count', 'one_star_count', 'updated_at']
    
    actions = ['update_rating_summaries']
    
    def update_rating_summaries(self, request, queryset):
        for rating_summary in queryset:
            rating_summary.update_rating_summary()
        self.message_user(request, f'{queryset.count()} rating summaries updated.')
    update_rating_summaries.short_description = 'Update selected rating summaries'