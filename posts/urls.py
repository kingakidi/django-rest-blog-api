from django.urls import path
from . import views

urlpatterns = [
    path('', views.PostListView.as_view(), name='post-list'),
    path('<uuid:post_id>/', views.PostDetailView.as_view(), name='post-detail'),
    path('<uuid:post_id>/like/', views.PostLikeView.as_view(), name='post-like'),
    path('<uuid:post_id>/likes/', views.PostLikesListView.as_view(), name='post-likes-list'),
]
