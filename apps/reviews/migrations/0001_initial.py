# Generated by Django 4.2.7 on 2025-07-20 03:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 Star - Poor'), (2, '2 Stars - Fair'), (3, '3 Stars - Good'), (4, '4 Stars - Very Good'), (5, '5 Stars - Excellent')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_verified_purchase', models.BooleanField(default=False)),
                ('is_approved', models.BooleanField(default=True)),
                ('is_featured', models.BooleanField(default=False)),
                ('helpful_count', models.PositiveIntegerField(default=0)),
                ('image1', models.ImageField(blank=True, null=True, upload_to='review_images/')),
                ('image2', models.ImageField(blank=True, null=True, upload_to='review_images/')),
                ('image3', models.ImageField(blank=True, null=True, upload_to='review_images/')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='products.product')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews_written', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review',
                'verbose_name_plural': 'Reviews',
                'ordering': ['-created_at'],
                'unique_together': {('product', 'reviewer')},
            },
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('average_rating', models.DecimalField(decimal_places=2, default=0.0, max_digits=3)),
                ('total_reviews', models.PositiveIntegerField(default=0)),
                ('five_star_count', models.PositiveIntegerField(default=0)),
                ('four_star_count', models.PositiveIntegerField(default=0)),
                ('three_star_count', models.PositiveIntegerField(default=0)),
                ('two_star_count', models.PositiveIntegerField(default=0)),
                ('one_star_count', models.PositiveIntegerField(default=0)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating_summary', to='products.product')),
            ],
            options={
                'verbose_name': 'Product Rating Summary',
                'verbose_name_plural': 'Product Rating Summaries',
            },
        ),
        migrations.CreateModel(
            name='ReviewReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.CharField(choices=[('spam', 'Spam or fake review'), ('inappropriate', 'Inappropriate content'), ('offensive', 'Offensive language'), ('irrelevant', 'Not relevant to product'), ('personal', 'Personal information shared'), ('other', 'Other reason')], max_length=20)),
                ('description', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('is_resolved', models.BooleanField(default=False)),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('reporter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('resolved_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resolved_reports', to=settings.AUTH_USER_MODEL)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reports', to='reviews.review')),
            ],
            options={
                'verbose_name': 'Review Report',
                'verbose_name_plural': 'Review Reports',
                'ordering': ['-created_at'],
                'unique_together': {('review', 'reporter')},
            },
        ),
        migrations.CreateModel(
            name='ReviewHelpful',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('review', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='helpful_votes', to='reviews.review')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Review Helpful Vote',
                'verbose_name_plural': 'Review Helpful Votes',
                'unique_together': {('review', 'user')},
            },
        ),
    ]
