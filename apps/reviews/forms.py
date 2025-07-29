from django import forms
from .models import Review, ReviewReport


class ReviewForm(forms.ModelForm):
    """
    Form for creating and editing product reviews
    """
    class Meta:
        model = Review
        fields = ['rating', 'title', 'content', 'image1', 'image2', 'image3']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Summarize your review in a few words...',
                'required': True,
                'maxlength': 200
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Share your experience with this product. What did you like or dislike? How was the quality, delivery, and overall experience?',
                'required': True
            }),
            'image1': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'image3': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Overall Rating'
        self.fields['title'].label = 'Review Title'
        self.fields['content'].label = 'Your Review'
        self.fields['image1'].label = 'Photo 1 (optional)'
        self.fields['image2'].label = 'Photo 2 (optional)'
        self.fields['image3'].label = 'Photo 3 (optional)'
        
        # Add help text
        self.fields['rating'].help_text = 'Rate this product from 1 (poor) to 5 (excellent) stars'
        self.fields['image1'].help_text = 'Upload photos to help other buyers (JPG, PNG, max 5MB each)'

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 5:
            raise forms.ValidationError('Review title must be at least 5 characters long.')
        return title.strip() if title else title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content.strip()) < 20:
            raise forms.ValidationError('Review content must be at least 20 characters long.')
        return content.strip() if content else content


class QuickRatingForm(forms.Form):
    """
    Simple form for quick rating without full review
    """
    rating = forms.ChoiceField(
        choices=Review.RATING_CHOICES,
        widget=forms.Select(attrs={
            'class': 'form-control'
        }),
        label='Rate this product'
    )


class ReportReviewForm(forms.ModelForm):
    """
    Form for reporting inappropriate reviews
    """
    class Meta:
        model = ReviewReport
        fields = ['reason', 'description']
        widgets = {
            'reason': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Please provide additional details about why you are reporting this review...'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['reason'].label = 'Reason for reporting'
        self.fields['description'].label = 'Additional details (optional)'
        self.fields['description'].required = False


class ReviewFilterForm(forms.Form):
    """
    Form for filtering reviews
    """
    RATING_FILTER_CHOICES = [
        ('', 'All Ratings'),
        ('5', '5 Stars'),
        ('4', '4 Stars'),
        ('3', '3 Stars'),
        ('2', '2 Stars'),
        ('1', '1 Star'),
    ]
    
    SORT_CHOICES = [
        ('-created_at', 'Most Recent'),
        ('created_at', 'Oldest First'),
        ('-rating', 'Highest Rated'),
        ('rating', 'Lowest Rated'),
        ('-helpful_count', 'Most Helpful'),
    ]

    rating = forms.ChoiceField(
        choices=RATING_FILTER_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'form-control form-control-sm'
        })
    )
    
    verified_only = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Verified purchases only'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].label = 'Filter by rating'
        self.fields['sort_by'].label = 'Sort by'


class ReviewSearchForm(forms.Form):
    """
    Form for searching reviews
    """
    query = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search reviews...'
        }),
        label=''
    )