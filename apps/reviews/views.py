from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg, Count
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator

from .models import Review, ReviewReport, ReviewHelpful, ProductRating
from .forms import ReviewForm, ReportReviewForm, ReviewFilterForm, QuickRatingForm
from apps.products.models import Product


class ReviewListView(ListView):
    """
    List all reviews for a specific product
    """
    model = Review
    template_name = 'reviews/review_list.html'
    context_object_name = 'reviews'
    paginate_by = 10

    def get_queryset(self):
        self.product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        queryset = Review.objects.filter(
            product=self.product,
            is_approved=True
        ).select_related('reviewer').order_by('-created_at')
        
        # Apply filters
        form = ReviewFilterForm(self.request.GET)
        if form.is_valid():
            rating = form.cleaned_data.get('rating')
            sort_by = form.cleaned_data.get('sort_by')
            verified_only = form.cleaned_data.get('verified_only')
            
            if rating:
                queryset = queryset.filter(rating=rating)
            
            if verified_only:
                queryset = queryset.filter(is_verified_purchase=True)
            
            if sort_by:
                queryset = queryset.order_by(sort_by)
        
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['filter_form'] = ReviewFilterForm(self.request.GET)
        context['page_title'] = f'Reviews for {self.product.title}'
        
        # Get or create rating summary
        rating_summary, created = ProductRating.objects.get_or_create(
            product=self.product
        )
        if created or not rating_summary.total_reviews:
            rating_summary.update_rating_summary()
        
        context['rating_summary'] = rating_summary
        context['rating_distribution'] = rating_summary.get_rating_distribution()
        
        # Check if user can review this product
        if self.request.user.is_authenticated:
            context['user_can_review'] = not Review.objects.filter(
                product=self.product,
                reviewer=self.request.user
            ).exists()
            
            # Get user's existing review if any
            try:
                context['user_review'] = Review.objects.get(
                    product=self.product,
                    reviewer=self.request.user
                )
            except Review.DoesNotExist:
                context['user_review'] = None
            
            # Add helpful status to reviews
            for review in context['reviews']:
                review.is_helpful_by_current_user = review.is_helpful_by_user(self.request.user)
        
        return context


class ReviewCreateView(LoginRequiredMixin, CreateView):
    """
    Create a new review for a product
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def dispatch(self, request, *args, **kwargs):
        self.product = get_object_or_404(Product, pk=self.kwargs['product_id'])
        
        # Check if user already reviewed this product
        if Review.objects.filter(product=self.product, reviewer=request.user).exists():
            messages.warning(request, 'You have already reviewed this product.')
            return redirect('reviews:review_list', product_id=self.product.pk)
        
        # Check if user is trying to review their own product
        if hasattr(self.product, 'seller') and self.product.seller == request.user:
            messages.error(request, 'You cannot review your own product.')
            return redirect('products:product_detail', pk=self.product.pk)
        
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.product = self.product
        form.instance.reviewer = self.request.user
        
        # Check if this is a verified purchase (implement based on your order system)
        # form.instance.is_verified_purchase = self.check_verified_purchase()
        
        response = super().form_valid(form)
        
        # Update product rating summary
        rating_summary, created = ProductRating.objects.get_or_create(
            product=self.product
        )
        rating_summary.update_rating_summary()
        
        messages.success(self.request, 'Thank you for your review!')
        return response

    def get_success_url(self):
        return reverse('reviews:review_list', kwargs={'product_id': self.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.product
        context['page_title'] = f'Write Review for {self.product.title}'
        return context


class ReviewUpdateView(LoginRequiredMixin, UpdateView):
    """
    Update an existing review
    """
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/review_form.html'

    def get_queryset(self):
        return Review.objects.filter(reviewer=self.request.user)

    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Update product rating summary
        rating_summary, created = ProductRating.objects.get_or_create(
            product=self.object.product
        )
        rating_summary.update_rating_summary()
        
        messages.success(self.request, 'Your review has been updated!')
        return response

    def get_success_url(self):
        return reverse('reviews:review_list', kwargs={'product_id': self.object.product.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self.object.product
        context['page_title'] = f'Edit Review for {self.object.product.title}'
        context['is_edit'] = True
        return context


class UserReviewsView(LoginRequiredMixin, ListView):
    """
    List all reviews written by the current user
    """
    model = Review
    template_name = 'reviews/user_reviews.html'
    context_object_name = 'reviews'
    paginate_by = 20

    def get_queryset(self):
        return Review.objects.filter(
            reviewer=self.request.user
        ).select_related('product').order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'My Reviews'
        
        # Get review statistics
        reviews = self.get_queryset()
        context['total_reviews'] = reviews.count()
        context['average_rating'] = reviews.aggregate(
            avg_rating=Avg('rating')
        )['avg_rating'] or 0
        
        return context


@login_required
@require_POST
def toggle_helpful(request):
    """
    AJAX endpoint to toggle helpful vote for a review
    """
    review_id = request.POST.get('review_id')
    
    try:
        review = get_object_or_404(Review, pk=review_id)
        
        # Check if user already voted
        helpful_vote, created = ReviewHelpful.objects.get_or_create(
            review=review,
            user=request.user
        )
        
        if not created:
            # User already voted, remove vote
            helpful_vote.delete()
            action = 'removed'
        else:
            action = 'added'
        
        # Update helpful count
        review.helpful_count = review.helpful_votes.count()
        review.save()
        
        return JsonResponse({
            'status': 'success',
            'action': action,
            'helpful_count': review.helpful_count
        })
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


@login_required
def report_review(request, review_id):
    """
    Report an inappropriate review
    """
    review = get_object_or_404(Review, pk=review_id)
    
    # Check if user already reported this review
    if ReviewReport.objects.filter(review=review, reporter=request.user).exists():
        messages.warning(request, 'You have already reported this review.')
        return redirect('reviews:review_list', product_id=review.product.pk)
    
    if request.method == 'POST':
        form = ReportReviewForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.review = review
            report.reporter = request.user
            report.save()
            
            messages.success(request, 'Thank you for reporting this review. We will investigate it.')
            return redirect('reviews:review_list', product_id=review.product.pk)
    else:
        form = ReportReviewForm()
    
    return render(request, 'reviews/report_review.html', {
        'form': form,
        'review': review,
        'page_title': 'Report Review'
    })


@login_required
def delete_review(request, pk):
    """
    Delete user's own review
    """
    review = get_object_or_404(Review, pk=pk, reviewer=request.user)
    product = review.product
    
    if request.method == 'POST':
        review.delete()
        
        # Update product rating summary
        rating_summary, created = ProductRating.objects.get_or_create(
            product=product
        )
        rating_summary.update_rating_summary()
        
        messages.success(request, 'Your review has been deleted.')
        return redirect('reviews:review_list', product_id=product.pk)
    
    return render(request, 'reviews/delete_review.html', {
        'review': review,
        'page_title': 'Delete Review'
    })


def review_detail(request, pk):
    """
    Display individual review detail
    """
    review = get_object_or_404(
        Review.objects.select_related('reviewer', 'product'),
        pk=pk,
        is_approved=True
    )
    
    # Add helpful status for current user
    if request.user.is_authenticated:
        review.is_helpful_by_current_user = review.is_helpful_by_user(request.user)
    
    return render(request, 'reviews/review_detail.html', {
        'review': review,
        'page_title': f'Review by {review.reviewer.username}'
    })