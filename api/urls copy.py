# api/urls.py

from django.urls import path
from .views import MessageListCreateView, ProfileListCreateView, UserListCreateView, PostListCreateView, CommentListCreateView

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('comments/', CommentListCreateView.as_view(), name='comment-list-create'),
     path('profiles/', ProfileListCreateView.as_view(), name='profile-list-create'),
       path('messages/', MessageListCreateView.as_view(), name='message-list-create'),
]
