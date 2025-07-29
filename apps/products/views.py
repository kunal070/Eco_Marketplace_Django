from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Q, Avg, Count
from .models import Product, Category, ProductImage, ProductFavorite
from .forms import ProductForm, ProductSearchForm

from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404


from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

class ProductListView(ListView):
    """
    List all products with filtering and search
    """
    model = Product
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True, is_approved=True).select_related(
            'category', 'seller'
        ).prefetch_related('images').annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
        
        # Search functionality
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(category__name__icontains=q) |
                Q(seller__username__icontains=q)
            )
        
        # Category filter
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Price range filter
        min_price = self.request.GET.get('min_price')
        max_price = self.request.GET.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Rating filter
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(average_rating__gte=rating)
        
        # Sort options
        sort_by = self.request.GET.get('sort')
        if sort_by == 'price_low':
            queryset = queryset.order_by('price')
        elif sort_by == 'price_high':
            queryset = queryset.order_by('-price')
        elif sort_by == 'rating':
            queryset = queryset.order_by('-average_rating')
        elif sort_by == 'newest':
            queryset = queryset.order_by('-created_at')
        else:
            queryset = queryset.order_by('-created_at')
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['page_title'] = 'Products'
        
        # Add favorite status for authenticated users
        if self.request.user.is_authenticated:
            for product in context['products']:
                product.is_favorited_by_user = ProductFavorite.objects.filter(
                    product=product, user=self.request.user
                ).exists()
        
        return context

class ProductDetailView(DetailView):
    """
    Display individual product details
    """
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_queryset(self):
        return Product.objects.filter(is_active=True, is_approved=True).select_related(
            'category', 'seller'
        ).prefetch_related('images').annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.get_object()
        
        # Add favorite status for authenticated users
        if self.request.user.is_authenticated:
            context['is_favorited'] = ProductFavorite.objects.filter(
                product=product, user=self.request.user
            ).exists()
        
        # Get related products
        context['related_products'] = Product.objects.filter(
            category=product.category,
            is_active=True,
            is_approved=True
        ).exclude(pk=product.pk).annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )[:4]
        
        context['page_title'] = product.title
        return context

class CategoryDetailView(ListView):
    """
    Display products in a specific category
    """
    model = Product
    template_name = 'products/category_detail.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        self.category = Category.objects.get(slug=self.kwargs['slug'])
        return Product.objects.filter(
            category=self.category,
            is_active=True,
            is_approved=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['page_title'] = f'Products in {self.category.name}'
        return context

class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new product
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'
    success_url = reverse_lazy('products:product_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Sell Your Product'
        context['is_create'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your product has been listed successfully!')
        return super().form_valid(form)

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing product
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/product_form.html'

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Edit Product'
        context['is_edit'] = True
        return context

    def form_valid(self, form):
        messages.success(self.request, 'Your product has been updated successfully!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('products:product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/product_confirm_delete.html'
    success_url = reverse_lazy('products:product_list')

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your product has been deleted successfully!')
        return super().delete(request, *args, **kwargs)

class MyProductsView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'products/my_products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Products'
        return context

class CategoryListView(ListView):
    model = Category
    template_name = 'products/category_list.html'
    context_object_name = 'categories'
    paginate_by = 20

    def get_queryset(self):
        return Category.objects.filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Browse Categories'
        return context

class SearchResultsView(ListView):
    model = Product
    template_name = 'products/search_results.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        form = ProductSearchForm(self.request.GET)
        queryset = Product.objects.filter(is_active=True, is_approved=True)
        if form.is_valid():
            q = form.cleaned_data.get('q')
            if q:
                queryset = queryset.filter(
                    Q(title__icontains=q) |
                    Q(description__icontains=q) |
                    Q(category__name__icontains=q) |
                    Q(seller__username__icontains=q)
                )
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            min_price = form.cleaned_data.get('min_price')
            if min_price is not None:
                queryset = queryset.filter(price__gte=min_price)
            max_price = form.cleaned_data.get('max_price')
            if max_price is not None:
                queryset = queryset.filter(price__lte=max_price)
            condition = form.cleaned_data.get('condition')
            if condition:
                queryset = queryset.filter(condition=condition)
            sort_by = form.cleaned_data.get('sort_by')
            if sort_by == 'price_low':
                queryset = queryset.order_by('price')
            elif sort_by == 'price_high':
                queryset = queryset.order_by('-price')
            elif sort_by == 'rating':
                queryset = queryset.order_by('-average_rating')
            else:
                queryset = queryset.order_by('-created_at')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = ProductSearchForm(self.request.GET)
        context['page_title'] = 'Search Results'
        return context

class MyFavoritesView(LoginRequiredMixin, ListView):
    """
    Display user's favorite products
    """
    model = Product
    template_name = 'products/my_favorites.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        # Get products that the user has favorited
        favorite_products = ProductFavorite.objects.filter(
            user=self.request.user
        ).values_list('product_id', flat=True)
        
        return Product.objects.filter(
            id__in=favorite_products,
            is_active=True,
            is_approved=True
        ).select_related('category', 'seller').prefetch_related('images').annotate(
            average_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Favorites'
        context['favorites_count'] = self.get_queryset().count()
        
        # Mark all as favorited since this is favorites page
        for product in context['products']:
            product.is_favorited_by_user = True
            
        return context

@require_POST
def toggle_favorite(request, product_id):
    """
    AJAX endpoint to toggle favorite status for a product
    """
    try:
        product = get_object_or_404(Product, pk=product_id)
        favorite, created = ProductFavorite.objects.get_or_create(
            product=product,
            user=request.user
        )
        
        if not created:
            favorite.delete()
            action = 'removed'
        else:
            action = 'added'
        
        return JsonResponse({
            'status': 'success',
            'action': action
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

@login_required
@require_POST
def mark_as_sold(request, product_id):
    """
    AJAX endpoint to mark a product as sold/unsold
    """
    try:
        product = get_object_or_404(Product, pk=product_id, seller=request.user)
        
        # Toggle the active status
        product.is_active = not product.is_active
        product.save(update_fields=['is_active'])
        
        status = 'available' if product.is_active else 'sold'
        message = f'Product marked as {status}'
        
        return JsonResponse({
            'status': 'success',
            'action': status,
            'message': message,
            'is_active': product.is_active
        })
    
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)