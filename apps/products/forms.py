from django import forms
from .models import Product, ProductImage, Category


class ProductForm(forms.ModelForm):
    """
    Form for creating and editing products
    """
    images = forms.FileField(
        required=False,
        help_text="Upload an image for your product."
    )
    
    class Meta:
        model = Product
        fields = [
            'title', 'description', 'category', 'price', 
            'condition', 'location', 'is_negotiable'
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter product title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe your product in detail...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-select'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0'
            }),
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, State'
            }),
            'is_negotiable': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        
        # Make category required
        self.fields['category'].empty_label = "Select a category"
        
        # Add help text
        self.fields['title'].help_text = "Choose a clear, descriptive title"
        self.fields['description'].help_text = "Include details about condition, features, and any defects"
        self.fields['price'].help_text = "Set a fair price for your item"
        self.fields['location'].help_text = "Your city and state for local buyers"

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title and len(title.strip()) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")
        return title.strip()

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if description and len(description.strip()) < 20:
            raise forms.ValidationError("Description must be at least 20 characters long.")
        return description.strip()

    def save(self, commit=True):
        product = super().save(commit=False)
        if self.user:
            product.seller = self.user
        
        if commit:
            product.save()
            
            # Handle image upload
            image = self.files.get('images')
            if image:
                ProductImage.objects.create(
                    product=product,
                    image=image,
                    is_main=True
                )
        
        return product


class ProductImageForm(forms.ModelForm):
    """
    Form for adding additional images to a product
    """
    class Meta:
        model = ProductImage
        fields = ['image']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }


class ProductSearchForm(forms.Form):
    """
    Form for product search and filtering
    """
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search products...'
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=None,
        required=False,
        empty_label="All Categories",
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    min_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Price'
        })
    )
    
    max_price = forms.DecimalField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Price'
        })
    )
    
    condition = forms.ChoiceField(
        choices=[('', 'Any Condition')] + Product.CONDITION_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    sort_by = forms.ChoiceField(
        choices=[
            ('newest', 'Newest First'),
            ('price_low', 'Price: Low to High'),
            ('price_high', 'Price: High to Low'),
            ('rating', 'Highest Rated'),
        ],
        required=False,
        initial='newest',
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Category
        self.fields['category'].queryset = Category.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        min_price = cleaned_data.get('min_price')
        max_price = cleaned_data.get('max_price')
        
        if min_price and max_price and min_price > max_price:
            raise forms.ValidationError("Minimum price cannot be greater than maximum price.")
        
        return cleaned_data

# Aliases for clarity
ProductCreateForm = ProductForm
ProductEditForm = ProductForm

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image', 'parent', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'parent': forms.Select(attrs={'class': 'form-select'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AdvancedSearchForm(ProductSearchForm):
    # Extend or alias ProductSearchForm for advanced search if needed
    pass
