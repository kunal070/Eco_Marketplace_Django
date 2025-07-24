from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from apps.products.models import Category, Product, ProductImage
from apps.messaging.models import Conversation, Message
from apps.reviews.models import Review, ProductRating
import random


class Command(BaseCommand):
    help = 'Create sample data for testing messaging and reviews systems'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create test users
        users = []
        for i in range(1, 6):
            username = f'user{i}'
            email = f'user{i}@example.com'
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'User{i}',
                    'last_name': 'Test',
                    'is_active': True
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                self.stdout.write(f'Created user: {username}')
            users.append(user)
        
        # Create categories
        categories = []
        category_names = ['Electronics', 'Furniture', 'Clothing', 'Books', 'Sports']
        for name in category_names:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'slug': name.lower(),
                    'description': f'Sample {name} category'
                }
            )
            if created:
                self.stdout.write(f'Created category: {name}')
            categories.append(category)
        
        # Create products
        products = []
        product_data = [
            ('iPhone 12', 'Excellent condition iPhone 12, 128GB', 599.99, 'Electronics'),
            ('Wooden Desk', 'Solid wood desk, perfect for home office', 299.99, 'Furniture'),
            ('Nike Sneakers', 'Barely used Nike running shoes, size 10', 89.99, 'Sports'),
            ('Python Programming Book', 'Learn Python programming, like new', 25.99, 'Books'),
            ('Leather Jacket', 'Vintage leather jacket, great condition', 199.99, 'Clothing'),
        ]
        
        for title, description, price, category_name in product_data:
            category = next(c for c in categories if c.name == category_name)
            seller = random.choice(users)
            
            product, _ = Product.objects.get_or_create(
                title=title,
                defaults={
                    'slug': title.lower().replace(' ', '-'),
                    'description': description,
                    'short_description': description[:100],
                    'seller': seller,
                    'category': category,
                    'price': price,
                    'condition': random.choice(['new', 'like_new', 'excellent', 'good']),
                    'location': 'New York, NY',
                    'city': 'New York',
                    'state': 'NY',
                    'is_active': True,
                    'is_approved': True
                }
            )
            # Always set or update the main image
            image_urls = {
                'iPhone 12': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=600&q=80',
                'Wooden Desk': 'https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?auto=format&fit=crop&w=600&q=80',
                'Nike Sneakers': 'https://images.pexels.com/photos/2529147/pexels-photo-2529147.jpeg?auto=compress&cs=tinysrgb&fit=crop&w=600&q=80',
                'Python Programming Book': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&w=600&q=80',
                'Leather Jacket': 'https://images.unsplash.com/photo-1512436991641-6745cdb1723f?auto=format&fit=crop&w=600&q=80',
            }
            main_img, created = ProductImage.objects.get_or_create(
                product=product,
                is_main=True,
                defaults={
                    'remote_image_url': image_urls.get(title, 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80')
                }
            )
            if not created:
                main_img.remote_image_url = image_urls.get(title, 'https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=600&q=80')
                main_img.save()
            products.append(product)
        
        # Create conversations and messages
        for i in range(5):
            participants = random.sample(users, 2)
            conversation = Conversation.objects.create(
                subject=f'Sample conversation {i+1}',
                created_at=timezone.now() - timezone.timedelta(days=random.randint(1, 30))
            )
            conversation.participants.set(participants)
            
            # Create messages
            for j in range(random.randint(2, 5)):
                sender = random.choice(participants)
                Message.objects.create(
                    conversation=conversation,
                    sender=sender,
                    content=f'This is message {j+1} in conversation {i+1}. Sample content for testing.',
                    created_at=timezone.now() - timezone.timedelta(hours=random.randint(1, 24))
                )
            
            self.stdout.write(f'Created conversation: {conversation.subject}')
        
        # Create reviews
        for product in products:
            # Create 2-4 reviews per product
            for i in range(random.randint(2, 4)):
                reviewer = random.choice(users)
                if reviewer != product.seller:  # Don't let seller review their own product
                    review, created = Review.objects.get_or_create(
                        product=product,
                        reviewer=reviewer,
                        defaults={
                            'rating': random.randint(3, 5),
                            'title': f'Great {product.title}',
                            'content': f'This is a sample review for {product.title}. The product is in good condition and works as expected. Would recommend!',
                            'is_approved': True,
                            'is_verified_purchase': random.choice([True, False])
                        }
                    )
                    if created:
                        self.stdout.write(f'Created review for {product.title} by {reviewer.username}')
        
        # Update product rating summaries
        for product in products:
            rating_summary, created = ProductRating.objects.get_or_create(product=product)
            rating_summary.update_rating_summary()
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created sample data:\n'
                f'- {len(users)} users\n'
                f'- {len(categories)} categories\n'
                f'- {len(products)} products\n'
                f'- 5 conversations with messages\n'
                f'- Multiple reviews per product\n'
                f'\nYou can now test the messaging and reviews systems!'
            )
        ) 