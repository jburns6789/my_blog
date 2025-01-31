from rest_framework import serializers
from .models import Post, Comment, Category, Tag    

class PostSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()
    tags = serializers.StringRelatedField(many=True)
    author = serializers.StringRelatedField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'slug', 'author', 'content', 'publish', 'status', 'category', 'tags']

class CommentSerializer(serializers.ModelSerializer):
    post = serializers.StringRelatedField()

    class Meta:
        fields = ['id', 'post', 'name', 'email', 'body', 'created', 'active']