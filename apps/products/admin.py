from django.contrib import admin
from .models import Category, Product, ProductImage, ProductFavorite, ProductView


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_active', 'get_products_count', 'created_at']
    list_filter = ['is_active', 'parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    def get_products_count(self, obj):
        return obj.get_products_count()
    get_products_count.short_description = 'Products Count'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'category', 'price', 'condition', 'location', 'is_active', 'is_featured', 'is_approved', 'views_count', 'created_at']
    list_filter = ['is_active', 'is_featured', 'is_approved', 'condition', 'category', 'created_at']
    search_fields = ['title', 'description', 'seller__username', 'location']
    list_editable = ['is_active', 'is_featured', 'is_approved']
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'description', 'short_description', 'seller', 'category')
        }),
        ('Pricing', {
            'fields': ('price', 'original_price', 'is_negotiable')
        }),
        ('Product Details', {
            'fields': ('condition', 'brand', 'model', 'year')
        }),
        ('Location', {
            'fields': ('location', 'city', 'state', 'zip_code')
        }),
        ('Status', {
            'fields': ('is_active', 'is_featured', 'is_approved')
        }),
        ('Statistics', {
            'fields': ('views_count', 'favorites_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['views_count', 'favorites_count', 'created_at', 'updated_at']
    
    actions = ['approve_products', 'feature_products', 'unfeature_products']
    
    def approve_products(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f'{queryset.count()} products approved.')
    approve_products.short_description = 'Approve selected products'
    
    def feature_products(self, request, queryset):
        queryset.update(is_featured=True)
        self.message_user(request, f'{queryset.count()} products featured.')
    feature_products.short_description = 'Feature selected products'
    
    def unfeature_products(self, request, queryset):
        queryset.update(is_featured=False)
        self.message_user(request, f'{queryset.count()} products unfeatured.')
    unfeature_products.short_description = 'Unfeature selected products'


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['product', 'image', 'is_main', 'caption', 'created_at']
    list_filter = ['is_main', 'created_at']
    search_fields = ['product__title', 'caption']
    list_editable = ['is_main', 'caption']
    readonly_fields = ['created_at']


@admin.register(ProductFavorite)
class ProductFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'product__title']
    readonly_fields = ['created_at']


@admin.register(ProductView)
class ProductViewAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'session_key', 'ip_address', 'viewed_at']
    list_filter = ['product', 'user', 'viewed_at']
    search_fields = ['product__title', 'user__username', 'ip_address', 'session_key']
    readonly_fields = ['viewed_at']
