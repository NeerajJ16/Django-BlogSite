from django.contrib import admin
from blog.models import Post, BlogCommet

# Register your models here.
admin.site.register((Post, BlogCommet))