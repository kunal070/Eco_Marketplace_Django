from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils import timezone


class Review(models.Model):
    """
    Model for user reviews of products
    """
    RATING_CHOICES = [
        (1, '1 Star - Poor'),
        (2, '2 Stars - Fair'),
        (3, '3 Stars - Good'),
        (4, '4 Stars - Very Good'),
        (5, '5 Stars - Excellent'),
    ]

    # Core fields
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    reviewer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews_written'
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    content = models.TextField()
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status and moderation
    is_verified_purchase = models.BooleanField(default=False)
    is_approved = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    
    # Helpful votes
    helpful_count = models.PositiveIntegerField(default=0)
    
    # Optional: Review images
    image1 = models.ImageField(upload_to='review_images/', null=True, blank=True)
    image2 = models.ImageField(upload_to='review_images/', null=True, blank=True)
    image3 = models.ImageField(upload_to='review_images/', null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = ('product', 'reviewer')  # One review per user per product
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return f"{self.reviewer.username} - {self.product.title} ({self.rating} stars)"

    def get_absolute_url(self):
        return reverse('reviews:review_detail', kwargs={'pk': self.pk})

    def get_star_display(self):
        """Return star rating as HTML"""
        full_stars = self.rating
        empty_stars = 5 - self.rating
        return '★' * full_stars + '☆' * empty_stars

    def get_star_percentage(self):
        """Return rating as percentage for CSS width"""
        return (self.rating / 5) * 100

    def is_helpful_by_user(self, user):
        """Check if user found this review helpful"""
        if user.is_authenticated:
            return self.helpful_votes.filter(user=user).exists()
        return False

    def get_review_images(self):
        """Get all review images as a list"""
        images = []
        for i in range(1, 4):
            image = getattr(self, f'image{i}')
            if image:
                images.append(image)
        return images


class ReviewHelpful(models.Model):
    """
    Model to track which users found reviews helpful
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='helpful_votes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('review', 'user')
        verbose_name = 'Review Helpful Vote'
        verbose_name_plural = 'Review Helpful Votes'

    def __str__(self):
        return f"{self.user.username} found review helpful"


class ReviewReport(models.Model):
    """
    Model for reporting inappropriate reviews
    """
    REPORT_REASONS = [
        ('spam', 'Spam or fake review'),
        ('inappropriate', 'Inappropriate content'),
        ('offensive', 'Offensive language'),
        ('irrelevant', 'Not relevant to product'),
        ('personal', 'Personal information shared'),
        ('other', 'Other reason'),
    ]

    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey(User, on_delete=models.CASCADE)
    reason = models.CharField(max_length=20, choices=REPORT_REASONS)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='resolved_reports'
    )

    class Meta:
        ordering = ['-created_at']
        unique_together = ('review', 'reporter')  # One report per user per review
        verbose_name = 'Review Report'
        verbose_name_plural = 'Review Reports'

    def __str__(self):
        return f"Report by {self.reporter.username} - {self.get_reason_display()}"

    def resolve(self, resolved_by_user):
        """Mark report as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.resolved_by = resolved_by_user
        self.save()


class ProductRating(models.Model):
    """
    Model to store aggregated rating data for products
    This helps with performance when displaying average ratings
    """
    product = models.OneToOneField(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='rating_summary'
    )
    
    # Rating statistics
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.PositiveIntegerField(default=0)
    
    # Rating distribution
    five_star_count = models.PositiveIntegerField(default=0)
    four_star_count = models.PositiveIntegerField(default=0)
    three_star_count = models.PositiveIntegerField(default=0)
    two_star_count = models.PositiveIntegerField(default=0)
    one_star_count = models.PositiveIntegerField(default=0)
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Product Rating Summary'
        verbose_name_plural = 'Product Rating Summaries'

    def __str__(self):
        return f"{self.product.title} - {self.average_rating} stars ({self.total_reviews} reviews)"

    def update_rating_summary(self):
        """Recalculate rating statistics from reviews"""
        reviews = self.product.reviews.filter(is_approved=True)
        
        self.total_reviews = reviews.count()
        
        if self.total_reviews > 0:
            # Calculate average
            total_rating = sum(review.rating for review in reviews)
            self.average_rating = round(total_rating / self.total_reviews, 2)
            
            # Count by rating
            self.five_star_count = reviews.filter(rating=5).count()
            self.four_star_count = reviews.filter(rating=4).count()
            self.three_star_count = reviews.filter(rating=3).count()
            self.two_star_count = reviews.filter(rating=2).count()
            self.one_star_count = reviews.filter(rating=1).count()
        else:
            self.average_rating = 0.00
            self.five_star_count = 0
            self.four_star_count = 0
            self.three_star_count = 0
            self.two_star_count = 0
            self.one_star_count = 0
        
        self.save()

    def get_rating_distribution(self):
        """Get rating distribution as percentages"""
        if self.total_reviews == 0:
            return {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        
        return {
            5: round((self.five_star_count / self.total_reviews) * 100, 1),
            4: round((self.four_star_count / self.total_reviews) * 100, 1),
            3: round((self.three_star_count / self.total_reviews) * 100, 1),
            2: round((self.two_star_count / self.total_reviews) * 100, 1),
            1: round((self.one_star_count / self.total_reviews) * 100, 1),
        }

    def get_star_display(self):
        """Return average rating as star display"""
        full_stars = int(self.average_rating)
        half_star = (self.average_rating - full_stars) >= 0.5
        empty_stars = 5 - full_stars - (1 if half_star else 0)
        
        display = '★' * full_stars
        if half_star:
            display += '☆'
        display += '☆' * empty_stars
        
        return display