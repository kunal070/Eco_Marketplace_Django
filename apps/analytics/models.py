from django.db import models
from django.contrib.auth.models import User

class VisitLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    page = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.IntegerField(default=0)  # duration in seconds

class VisitLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    path = models.CharField(max_length=255, default='unknown')  # OK
    timestamp = models.DateTimeField(auto_now_add=True)

    # Optional fields
    page = models.CharField(max_length=100, null=True, blank=True)
    duration = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} visited {self.path} at {self.timestamp}"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} searched '{self.query}' at {self.timestamp}"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=100)
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class PopularProduct(models.Model):
    product_name = models.CharField(max_length=255)
    views = models.IntegerField(default=0)
