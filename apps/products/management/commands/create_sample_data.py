# Then create __init__.py files in both directories

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from apps.products.models import Category, Product, ProductImage
from django.utils.text import slugify
import random

class Command(BaseCommand):
    help = 'Create sample data for the eco-friendly marketplace'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new data',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write(self.style.WARNING('Clearing existing data...'))
            Product.objects.all().delete()
            Category.objects.all().delete()
            
        self.stdout.write('Creating sample data...')

        # Create categories
        categories_data = [
            {
                'name': 'Solar Energy',
                'description': 'Solar panels, solar chargers, and renewable energy solutions',
                'slug': 'solar-energy'
            },
            {
                'name': 'Sustainable Fashion',
                'description': 'Eco-friendly clothing, organic textiles, and ethical fashion',
                'slug': 'sustainable-fashion'
            },
            {
                'name': 'Green Home & Garden',
                'description': 'Eco-friendly home products, organic gardening supplies',
                'slug': 'green-home-garden'
            },
            {
                'name': 'Recycled Electronics',
                'description': 'Refurbished electronics, upcycled tech, and eco gadgets',
                'slug': 'recycled-electronics'
            },
            {
                'name': 'Organic Food & Health',
                'description': 'Organic foods, natural supplements, and health products',
                'slug': 'organic-food-health'
            },
            {
                'name': 'Zero Waste Living',
                'description': 'Reusable products, zero waste solutions, and sustainable alternatives',
                'slug': 'zero-waste-living'
            },
        ]

        categories = []
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'description': cat_data['description'],
                    'slug': cat_data['slug'],
                    'is_active': True
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(f'Created category: {category.name}')

        # Create sample users
        sample_users = []
        user_data = [
            {'username': 'ecowarrior', 'email': 'eco@example.com', 'first_name': 'Eco', 'last_name': 'Warrior'},
            {'username': 'greenliving', 'email': 'green@example.com', 'first_name': 'Green', 'last_name': 'Living'},
            {'username': 'sustainableshop', 'email': 'sustainable@example.com', 'first_name': 'Sustainable', 'last_name': 'Shop'},
            {'username': 'earthfriendly', 'email': 'earth@example.com', 'first_name': 'Earth', 'last_name': 'Friendly'},
            {'username': 'zerowastehero', 'email': 'zerowaste@example.com', 'first_name': 'Zero', 'last_name': 'Waste'},
        ]

        for user_info in user_data:
            user, created = User.objects.get_or_create(
                username=user_info['username'],
                defaults={
                    'email': user_info['email'],
                    'first_name': user_info['first_name'],
                    'last_name': user_info['last_name'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            sample_users.append(user)

        # Create sample products
        products_data = [
            # Solar Energy Products
            {
                'title': '100W Portable Solar Panel Kit',
                'description': 'High-efficiency monocrystalline solar panel perfect for camping, RV, and off-grid applications. Includes charge controller and cables. Weather-resistant design with 25-year warranty.',
                'category': 'Solar Energy',
                'price': 299.99,
                'condition': 'new',
                'location': 'San Francisco, CA',
                'is_negotiable': False,
                'remote_image_url': 'https://images.unsplash.com/photo-1509391366360-2e959784a276?w=500'
            },
            {
                'title': 'Solar Phone Charger Power Bank',
                'description': 'Eco-friendly solar power bank with 20,000mAh capacity. Charges via solar or USB. Perfect for hiking and outdoor adventures. Waterproof and shockproof design.',
                'category': 'Solar Energy',
                'price': 89.99,
                'condition': 'like_new',
                'location': 'Portland, OR',
                'is_negotiable': True,
                'remote_image_url': 'https://images.unsplash.com/photo-1593941707882-a5bac6861d75?w=500'
            },
            
            # Sustainable Fashion
            {
                'title': 'Organic Cotton T-Shirt Collection',
                'description': 'Set of 3 organic cotton t-shirts made from 100% GOTS certified organic cotton. Soft, breathable, and dyed with natural colors. Available in various sizes.',
                'category': 'Sustainable Fashion',
                'price': 45.00,
                'condition': 'new',
                'location': 'Austin, TX',
                'is_negotiable': False,
                'remote_image_url': 'https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500'
            },
            {
                'title': 'Recycled Denim Jacket',
                'description': 'Vintage-style denim jacket made from 100% recycled denim. Unique patchwork design. Each piece is one-of-a-kind. Size Medium. Perfect for sustainable fashion lovers.',
                'category': 'Sustainable Fashion',
                'price': 75.00,
                'condition': 'excellent',
                'location': 'Brooklyn, NY',
                'is_negotiable': True,
                'remote_image_url': 'https://images.unsplash.com/photo-1551028719-00167b16eac5?w=500'
            },
            
            # Green Home & Garden
            {
                'title': 'Bamboo Kitchen Utensil Set',
                'description': 'Complete 12-piece bamboo kitchen utensil set. Naturally antimicrobial and sustainable. Includes spatulas, spoons, tongs, and storage holder. Perfect eco-friendly kitchen upgrade.',
                'category': 'Green Home & Garden',
                'price': 35.99,
                'condition': 'new',
                'location': 'Seattle, WA',
                'is_negotiable': False,
                'remote_image_url': 'https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=500'
            },
            {
                'title': 'Organic Vegetable Garden Starter Kit',
                'description': 'Everything you need to start your organic vegetable garden. Includes heirloom seeds (tomatoes, lettuce, herbs), organic soil, biodegradable pots, and growing guide.',
                'category': 'Green Home & Garden',
                'price': 55.00,
                'condition': 'new',
                'location': 'Denver, CO',
                'is_negotiable': True,
                'remote_image_url': 'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500'
            },
            
            # Recycled Electronics
            {
                'title': 'Refurbished MacBook Pro 13"',
                'description': 'Professionally refurbished MacBook Pro 13" (2019). Intel Core i5, 8GB RAM, 256GB SSD. Battery replaced, body restored. Comes with 6-month warranty. Carbon neutral shipping.',
                'category': 'Recycled Electronics',
                'price': 899.99,
                'condition': 'excellent',
                'location': 'Los Angeles, CA',
                'is_negotiable': True,
                'remote_image_url': 'https://images.unsplash.com/photo-1541807084-5c52b6b3adef?w=500'
            },
            {
                'title': 'Upcycled Smartphone Stand',
                'description': 'Handcrafted smartphone stand made from reclaimed wood and recycled metal. Adjustable angle, fits all phone sizes. Each piece is unique. Supports sustainable craftsmanship.',
                'category': 'Recycled Electronics',
                'price': 25.00,
                'condition': 'new',
                'location': 'Nashville, TN',
                'is_negotiable': False,
                'remote_image_url': 'https://images.unsplash.com/photo-1512499617640-c74ae3a79d37?w=500'
            },
            
            # Zero Waste Living
            {
                'title': 'Stainless Steel Reusable Straws Set',
                'description': 'Set of 4 stainless steel straws with cleaning brush and hemp carrying pouch. Straight and bent options. Dishwasher safe. Perfect for reducing plastic waste.',
                'category': 'Zero Waste Living',
                'price': 15.99,
                'condition': 'new',
                'location': 'San Diego, CA',
                'is_negotiable': False,
                'remote_image_url': 'https://images.unsplash.com/photo-1571115764595-644a1f56a55c?w=500'
            },
            {
                'title': 'Beeswax Food Wraps Set',
                'description': 'Plastic-free food storage solution. Set of 6 beeswax wraps in various sizes. Made with organic cotton, beeswax, pine resin, and jojoba oil. Reusable for up to a year.',
                'category': 'Zero Waste Living',
                'price': 28.00,
                'condition': 'new',
                'location': 'Burlington, VT',
                'is_negotiable': False,
                'remote_image_url': 'https://images.unsplash.com/photo-1610899922372-7e0e21108c7e?w=500'
            },
            
            # Organic Food & Health
            {
                'title': 'Organic Herbal Tea Collection',
                'description': 'Premium collection of 12 organic herbal teas. Includes chamomile, peppermint, ginger, and unique blends. Sustainably sourced, fair trade certified. Perfect for tea lovers.',
                'category': 'Organic Food & Health',
                'price': 42.00,
                'condition': 'new',
                'location': 'Asheville, NC',
                'is_negotiable': True,
                'remote_image_url': 'https://images.unsplash.com/photo-1556881286-bf4c2b1da32c?w=500'
            },
        ]

        # Create products
        for i, product_data in enumerate(products_data):
            # Find category
            category = next((cat for cat in categories if cat.name == product_data['category']), categories[0])
            
            # Random user
            seller = random.choice(sample_users)
            
            # Create product
            product, created = Product.objects.get_or_create(
                title=product_data['title'],
                defaults={
                    'slug': slugify(product_data['title']),
                    'description': product_data['description'],
                    'seller': seller,
                    'category': category,
                    'price': product_data['price'],
                    'condition': product_data['condition'],
                    'location': product_data['location'],
                    'city': product_data['location'].split(',')[0],
                    'state': product_data['location'].split(',')[1].strip() if ',' in product_data['location'] else '',
                    'is_negotiable': product_data['is_negotiable'],
                    'is_active': True,
                    'is_approved': True,
                }
            )
            
            if created:
                self.stdout.write(f'Created product: {product.title}')
                
                # Create product image with remote URL
                if 'remote_image_url' in product_data:
                    ProductImage.objects.create(
                        product=product,
                        remote_image_url=product_data['remote_image_url'],
                        is_main=True,
                        caption=f"Main image for {product.title}"
                    )
                    self.stdout.write(f'  Added image for: {product.title}')

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data!\n'
                f'Categories: {Category.objects.count()}\n'
                f'Products: {Product.objects.count()}\n'
                f'Users: {len(sample_users)}'
            )
        )