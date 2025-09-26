from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import (
    PostSerializer, PostCreateSerializer, PostUpdateSerializer, PostDetailSerializer
)


class PostPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostListView(APIView):
    permission_classes = [IsAuthenticated]
    pagination_class = PostPagination
    
    @extend_schema(
        tags=['Posts'],
        summary="List all posts",
        description="Get a paginated list of all blog posts",
        responses={
            200: PostSerializer(many=True),
            401: "Unauthorized"
        }
    )
    def get(self, request):
        posts = Post.objects.all()
        
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(posts, request)
        
        if page is not None:
            serializer = PostSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)
        
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Posts'],
        summary="Create a new post",
        description="Create a new blog post (authenticated users only)",
        request=PostCreateSerializer,
        responses={
            201: PostSerializer,
            400: "Bad Request - Validation errors",
            401: "Unauthorized"
        }
    )
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            post = serializer.save(author=request.user)
            response_serializer = PostSerializer(post)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=['Posts'],
        summary="Get post details",
        description="Get detailed information about a specific post including comments",
        responses={
            200: PostDetailSerializer,
            404: "Post not found",
            401: "Unauthorized"
        }
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        serializer = PostDetailSerializer(post)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Posts'],
        summary="Update post",
        description="Update a post (only by the author)",
        request=PostUpdateSerializer,
        responses={
            200: PostSerializer,
            400: "Bad Request - Validation errors",
            401: "Unauthorized",
            403: "Forbidden - Not the author",
            404: "Post not found"
        }
    )
    def put(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        if post.author != request.user:
            return Response(
                {'error': 'You can only edit your own posts'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = PostUpdateSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            response_serializer = PostSerializer(post)
            return Response(response_serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Posts'],
        summary="Delete post",
        description="Delete a post (only by the author)",
        responses={
            204: "Post deleted successfully",
            401: "Unauthorized",
            403: "Forbidden - Not the author",
            404: "Post not found"
        }
    )
    def delete(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        if post.author != request.user:
            return Response(
                {'error': 'You can only delete your own posts'}, 
                status=status.HTTP_403_FORBIDDEN
            )
        
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class PostLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    
    @extend_schema(
        tags=['Likes'],
        summary="Like/Unlike post",
        description="Like or unlike a post",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'liked': {'type': 'boolean'},
                    'likes_count': {'type': 'integer'}
                }
            },
            404: "Post not found",
            401: "Unauthorized"
        }
    )
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
            message = "Post unliked successfully"
        else:
            post.likes.add(request.user)
            liked = True
            message = "Post liked successfully"
        
        return Response({
            'message': message,
            'liked': liked,
            'likes_count': post.likes_count
        })


class PostLikesListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    
    @extend_schema(
        tags=['Likes'],
        summary="List post likes",
        description="Get list of users who liked a specific post",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'likes_count': {'type': 'integer'},
                    'liked_by': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'string'},
                                'email': {'type': 'string'},
                                'first_name': {'type': 'string'},
                                'last_name': {'type': 'string'},
                                'liked_at': {'type': 'string', 'format': 'date-time'}
                            }
                        }
                    }
                }
            },
            404: "Post not found",
            401: "Unauthorized"
        }
    )
    def get(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        
        likes_data = []
        for user in post.likes.all():
            likes_data.append({
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'liked_at': post.created_at.isoformat()
            })
        
        return Response({
            'likes_count': post.likes_count,
            'liked_by': likes_data
        })


