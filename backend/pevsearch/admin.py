from django.contrib import admin
from .models import CustomUser, Tag, Like, Bookmark, Post

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Tag)
admin.site.register(Like)
admin.site.register(Bookmark)
admin.site.register(Post)
