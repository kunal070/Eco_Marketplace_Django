from django.db import models
from django.contrib.auth.models import User

class VisitLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    path = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    duration = models.FloatField(null=True, blank=True)  # time spent on page in seconds

    def __str__(self):
        return f"{self.user} visited {self.path} at {self.timestamp}"

class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} searched '{self.query}' at {self.timestamp}"

class UserActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    detail = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.action} at {self.timestamp}"

class PopularProduct(models.Model):
    product_id = models.IntegerField()
    views = models.IntegerField(default=0)
    last_viewed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Product {self.product_id} - {self.views} views"
