from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from drf_spectacular.types import OpenApiTypes
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Comment
from .serializers import CommentSerializer, CommentCreateSerializer
from posts.models import Post


class CommentListView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=['Comments'],
        summary='List comments for a post',
        description='Get all comments for a specific post',
        parameters=[
            OpenApiParameter(
                name='post_id',
                type=OpenApiTypes.UUID,
                location=OpenApiParameter.QUERY,
                description='Post UUID',
                required=True
            )
        ],
        responses={
            200: CommentSerializer(many=True),
            404: {'description': 'Post not found'}
        }
    )
    def get(self, request):
        post_id = request.query_params.get('post_id')
        if not post_id:
            return Response(
                {'error': 'post_id parameter is required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        post = get_object_or_404(Post, id=post_id)
        comments = Comment.objects.filter(post=post)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        tags=['Comments'],
        summary='Create a comment',
        description='Create a new comment on a post',
        request=CommentCreateSerializer,
        responses={
            201: CommentSerializer,
            400: {'description': 'Invalid data'},
            404: {'description': 'Post not found'}
        }
    )
    def post(self, request):
        serializer = CommentCreateSerializer(data=request.data)
        
        if serializer.is_valid():
            post_id = serializer.validated_data['post_id']
            post = get_object_or_404(Post, id=post_id)
            
            with transaction.atomic():
                comment = serializer.save(
                    post=post,
                    author=request.user
                )
            response_serializer = CommentSerializer(comment)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    @extend_schema(
        tags=['Comments'],
        summary='Update a comment',
        description='Update a comment (author only)',
        request=CommentCreateSerializer,
        responses={
            200: CommentSerializer,
            400: {'description': 'Invalid data'},
            403: {'description': 'Permission denied'},
            404: {'description': 'Comment not found'}
        }
    )
    def put(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        
        if comment.author != request.user:
            return Response(
                {'error': 'You can only edit your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = CommentCreateSerializer(comment, data=request.data)
        
        if serializer.is_valid():
            with transaction.atomic():
                comment = serializer.save()
            response_serializer = CommentSerializer(comment)
            return Response(response_serializer.data)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Comments'],
        summary='Delete a comment',
        description='Delete a comment (author only)',
        responses={
            204: {'description': 'Comment deleted successfully'},
            403: {'description': 'Permission denied'},
            404: {'description': 'Comment not found'}
        }
    )
    def delete(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        
        if comment.author != request.user:
            return Response(
                {'error': 'You can only delete your own comments.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentLikeView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    
    @extend_schema(
        tags=['Likes'],
        summary="Like/Unlike comment",
        description="Like or unlike a comment",
        responses={
            200: {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'liked': {'type': 'boolean'},
                    'likes_count': {'type': 'integer'}
                }
            },
            404: "Comment not found",
            401: "Unauthorized"
        }
    )
    def post(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        
        if request.user in comment.likes.all():
            comment.likes.remove(request.user)
            liked = False
            message = "Comment unliked successfully"
        else:
            comment.likes.add(request.user)
            liked = True
            message = "Comment liked successfully"
        
        return Response({
            'message': message,
            'liked': liked,
            'likes_count': comment.likes_count
        })


class CommentLikesListView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    
    @extend_schema(
        tags=['Likes'],
        summary="List comment likes",
        description="Get list of users who liked a specific comment",
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
            404: "Comment not found",
            401: "Unauthorized"
        }
    )
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        
        likes_data = []
        for user in comment.likes.all():
            likes_data.append({
                'id': str(user.id),
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'liked_at': comment.created_at.isoformat()
            })
        
        return Response({
            'likes_count': comment.likes_count,
            'liked_by': likes_data
        })