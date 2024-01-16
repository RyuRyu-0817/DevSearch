from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostViewSet, basename="post")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = [
    path('', include(router.urls)),
    path("like/", like_post, name="like-post"),
    path("bookmark/", bookmark_post, name="bookmark-post"),
]


