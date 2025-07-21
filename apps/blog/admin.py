from django.contrib import admin
from .models import BlogPost, GreenTip, FAQ, Newsletter

admin.site.register(BlogPost)
admin.site.register(GreenTip)
admin.site.register(FAQ)
admin.site.register(Newsletter)
