from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field
from .models import Comment
from posts.models import Post
from authentication.serializers import UserSerializer


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    @extend_schema_field(serializers.IntegerField)
    def likes_count(self, obj):
        return obj.likes_count
    
    class Meta:
        model = Comment
        fields = ['id', 'body', 'author', 'likes_count', 'created_at']


class CommentCreateSerializer(serializers.ModelSerializer):
    post_id = serializers.UUIDField(write_only=True, required=True)
    body = serializers.CharField(required=True, min_length=3, max_length=1000)
    
    class Meta:
        model = Comment
        fields = ['body', 'post_id']
    
    def validate_body(self, value):
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Comment must be at least 3 characters long.")
        return value
    
    def validate_post_id(self, value):
        try:
            Post.objects.get(id=value)
        except Post.DoesNotExist:
            raise serializers.ValidationError("Post with this ID does not exist.")
        return value
