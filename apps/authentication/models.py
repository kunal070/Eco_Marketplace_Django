from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=15, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    preferences = models.CharField(
        max_length=20,
        choices=[
            ('fashion', 'Sustainable Fashion'),
            ('home', 'Eco Home & Garden'),
            ('tech', 'Green Technology'),
            ('food', 'Organic Food'),
            ('other', 'Other'),
        ],
        default='other',
        blank=True
    )
    is_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    phone_verification_code = models.CharField(max_length=6, blank=True, null=True)

    def __str__(self):
        return self.user.username