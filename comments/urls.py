from django.urls import path
from . import views

urlpatterns = [
    path('comments/', views.CommentListView.as_view(), name='comment-list'),
    path('comments/<uuid:comment_id>/', views.CommentDetailView.as_view(), name='comment-detail'),
    path('comments/<uuid:comment_id>/like/', views.CommentLikeView.as_view(), name='comment-like'),
    path('comments/<uuid:comment_id>/likes/', views.CommentLikesListView.as_view(), name='comment-likes-list'),
]
