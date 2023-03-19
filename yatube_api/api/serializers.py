from posts.models import Post, Group, Comment
from rest_framework import serializers
from djoser.serializers import UserSerializer
from django.contrib.auth.models import User


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ("email", "id", "username", "first_name", "last_name")


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        fields = ("id", "text", "author", "image", "pub_date")
        model = Post


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("id", "title", "slug", "description")


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ("id", "author", "post", "text", "created")
        model = Comment
