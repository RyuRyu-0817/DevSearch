from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()

router.register(r"users", UserViewSet, basename="user")
router.register(r"posts", PostViewSet, basename="post")
# router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"tags", TagViewSet, basename="tag")

urlpatterns = [
    path('', include(router.urls)),
    path("like/", like_post, name="like-post"),
    path("bookmark/", bookmark_post, name="bookmark-post"),
]



# urlpatterns = [
#     # ユーザ詳細、ユーザがいいねした記事一覧、ブックマークした記事一覧 〇
#     path("users/<int:pk>", UserViewSet.as_view({"get": "retrieve"}), name="user-detail"),
#     path("users/<int:pk>/like", UserLikeAPIView.as_view(), name="user-like"),
#     path("users/<int:pk>/bookmark", UserBookMarkAPIView.as_view(), name="user-bookmark"),

#     # 記事一覧、特定の記事に付随するコメント一覧　〇
#     path("posts/", PostViewSet.as_view({"get": "list"}), name="post-list"),

#     # コメント詳細の取得、更新、削除
#     path("posts/<int:pk>/comments/", CommentViewSet.as_view({"get": "list", "post": "create"})),
#     path("comments/<int:pk>/", CommentViewSet.as_view({
#         "get": "retrieve", 
#         "patch": "partial_update", 
#         "delete": "destroy",
#     })),

#     # タグ詳細、一覧
#     path("tags/", TagViewSet.as_view({"get": "list"}), name="tag-list"),
#     path("tags/<int:pk>/posts/", TagViewSet.as_view({"get": "retrieve"}), name="tag-detail"),
# ]
