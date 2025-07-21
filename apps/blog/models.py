from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class GreenTip(models.Model):
    tip = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()

class Newsletter(models.Model):
    email = models.EmailField()
    subscribed_on = models.DateTimeField(auto_now_add=True)
