from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Post
from authentication.models import User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_email = serializers.CharField(source='author.email', read_only=True)
    
    @extend_schema_field(serializers.IntegerField)
    def likes_count(self, obj):
        return obj.likes_count
    
    @extend_schema_field(serializers.IntegerField)
    def comments_count(self, obj):
        return obj.comments_count
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'body', 'cover_photo', 'author', 'author_email',
            'likes_count', 'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'cover_photo']
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value
    
    def validate_body(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Body must be at least 10 characters long")
        return value


class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'body', 'cover_photo']
    
    def validate_title(self, value):
        if len(value.strip()) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters long")
        return value
    
    def validate_body(self, value):
        if len(value.strip()) < 10:
            raise serializers.ValidationError("Body must be at least 10 characters long")
        return value


class PostDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    author_email = serializers.CharField(source='author.email', read_only=True)
    
    @extend_schema_field(serializers.IntegerField)
    def likes_count(self, obj):
        return obj.likes_count
    
    @extend_schema_field(serializers.IntegerField)
    def comments_count(self, obj):
        return obj.comments_count
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'body', 'cover_photo', 'author', 'author_email',
            'likes_count', 'comments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']
