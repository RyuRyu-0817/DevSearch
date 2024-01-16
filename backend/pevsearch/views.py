from django.shortcuts import render
from .models import *
from .serializer import *
from django.db.models import Q, Count
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import pagination
from dj_rest_auth.registration import serializers
from rest_framework import status
from rest_framework.decorators import api_view

# 個別のページネーション　ページサイズをクライアントから指定できるように
class PostNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'

class TagNumberPagination(pagination.PageNumberPagination):
    page_size_query_param = 'page_size'


# ここ変わるかも
class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
        /users  ユーザ一覧
        /users/pk/  ユーザー詳細
        /users/pk/like/  ユーザがいいねした記事
        /users/pk/bookmark/  ユーザがブックマークした記事
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["get"])
    def like(self, request, pk=None):
        user = self.get_object()
        queryset = Post.objects.filter(like__user_id=user.id).order_by("-site_Like")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["get"])
    def bookmark(self, request, pk=None):
        user = self.get_object()
        queryset = Post.objects.filter(bookmark__user_id=user.id).order_by("-site_Like")
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """
        /posts/  投稿一覧
        /posts/pk  投稿詳細
        /posts/pk/likes/  特定の投稿にいいねした人の一覧
    """

    queryset = Post.objects.all().order_by("-site_Like")
    serializer_class = PostSerializer
    
    @action(detail=True, methods=["get"])
    def likes(self, request, pk=None):
        post = self.get_object()
        queryset= CustomUser.objects.filter(like__post_id=post.id)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = UserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
    


    # getの検索機能
    def filter_queryset(self, queryset):
        keywords = self.request.query_params.get("keywords", None)
        if keywords:
            keywords = keywords.split()
            query = Q()
            for keyword in keywords:
                query |= Q(title__icontains=keyword)
                
            queryset = queryset.filter(query)
            
        return queryset 


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
        /tags/  タグ一覧
        /tags/pk/  タグ詳細
        /tags/pk/posts/  特定のタグの投稿一覧
    """

    queryset = Tag.objects.annotate(post_count=Count("post")).order_by("-post_count")
    serializer_class = TagSerializer
    pagination_class = TagNumberPagination


    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        


    # getの検索機能
    def filter_queryset(self, queryset):
        keywords = self.request.query_params.get("keywords", None)

        if keywords:
            # 戻り値がstr型になるからリスト型にする
            keywords = keywords.split()
            query = Q()
            for keyword in keywords:
                query |= Q(tagname__icontains=keyword)
            queryset = queryset.filter(query)

            
        return queryset
    


    @action(detail=True, methods=["get"])
    def posts(self, request, pk=None):
        tag = self.get_object()
        queryset = Post.objects.filter(tags=tag).order_by("-site_Like")

        pagination = PostNumberPagination()
        page = pagination.paginate_queryset(queryset, request)
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return pagination.get_paginated_response(serializer.data)

        serializer = PostSerializer(queryset, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def like_post(request):
    """
        /like/  ユーザがいいねするときのエンドポイント(POSTのみ)
    """

    user = CustomUser.objects.get(pk=request.data["user"]["pk"])
    post = Post.objects.get(id=request.data["post"]["id"])
    like, created = Like.objects.get_or_create(user=user, post=post)
    serializer = PostSerializer(post)

    if created:
        return Response({"is_liked": True, "post": serializer.data})
    else:
        like.delete()
        return Response({"is_liked": False, "post": serializer.data})
    
@api_view(['POST'])
def bookmark_post(request):
    """
        /bookmark/  ユーザがブックマークするときのエンドポイント(POSTのみ)
    """
    user = CustomUser.objects.get(pk=request.data["user"]["pk"])
    post = Post.objects.get(id=request.data["post"]["id"])
    bookmark, created = Bookmark.objects.get_or_create(user=user, post=post)
    serializer = PostSerializer(post)

    if created:
        return Response({"is_bookmarked": True, "post": serializer.data})
    else:
        bookmark.delete()
        return Response({"is_bookmarked": False, "post": serializer.data})
    

