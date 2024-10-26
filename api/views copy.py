# api/views.py

from myUser.models import Profile
from rest_framework import generics
from posts.models import Message, Post, Comment
from .serializers import MessageSerializer, ProfileSerializer, UserSerializer, PostSerializer, CommentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# Vues pour les utilisateurs
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Vues pour les posts
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# Vues pour les commentaires
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer


class ProfileListCreateView(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer    

class MessageListCreateView(generics.ListCreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer