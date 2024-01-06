from rest_framework import serializers
from .models import Post, Tag, Comment, CustomUser, Like, Bookmark
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("id", "username", "picture")
    

class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = "__all__"
    

class PostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
    like_count = serializers.SerializerMethodField()
    who_like = serializers.SerializerMethodField()
    who_bookmark = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "createdAt",
            "tags",
            "url",
            "image",
            "site_Like",
            "like_count",
            "who_like",
            "who_bookmark"
        ]
    

    def get_like_count(self, obj):
        like_count = obj.like_set.count()
        return like_count
    
    def get_who_like(self, obj):
        # いいねのシリアライザをつかったら、無限に再帰なる
        likes = obj.like_set.all().select_related('user')
        return UserSerializer([like.user for like in likes], many=True).data
    
    def get_who_bookmark(self, obj):
        # ブックマークのシリアライザをつかったら、無限に再帰なる
        bookmarks = obj.bookmark_set.all().select_related('user')
        return UserSerializer([bookmark.user for bookmark in bookmarks], many=True).data

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), write_only=True)

    class Meta:
        model = Comment
        fields = '__all__'  # または必要なフィールドを指定する

    def create(self, validated_data):
        validated_data["user"] = validated_data["user_id"]
        validated_data.pop("user_id")

        return Comment.objects.create(**validated_data)


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['name'] = user.username

        return token


class LikeSerializer(serializers.ModelSerializer):
    post = PostSerializer()

    class Meta:
        model = Like
        fields = [
            "post"
        ]

class BookMarkSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Bookmark
        fields = "__all__"
