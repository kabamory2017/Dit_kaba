# api/viewsets.py

from myUser.models import MyUser
from myUser.utils import send_welcome_email
from posts.models import Comment, Message, Post
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from django_filters import rest_framework as filters
from .serializers import ActivationTokenSerializer, MyUserSerializer, UserSerializer, PostSerializer, CommentSerializer, MessageSerializer
from django.contrib.auth import get_user_model

from rest_framework import permissions
from myUser.utils import send_welcome_email  # Importez la fonction
User = get_user_model()

# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
class CustomPagination(PageNumberPagination):
    page_size = 2  # Nombre d'objets par page
    page_size_query_param = 'page_size'  # Paramètre d'URL pour définir le nombre d'objets par page
    max_page_size = 100  # Limite maximum du nombre d'objets par page

# Filtrage pour les utilisateurs
class UserFilter(filters.FilterSet):
    email = filters.CharFilter(lookup_expr='icontains')  # Filtrer par email (insensible à la casse)

    class Meta:
        model = MyUser
        fields = ['email']  # Ajoutez d'autres champs que vous souhaitez filtrer

# ViewSet pour les utilisateurs
class UserViewSet(viewsets.ModelViewSet):
    queryset = MyUser.objects.all()
    serializer_class = ActivationTokenSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class = CustomPagination
    filterset_class = UserFilter  # Utilisation de la classe de filtre
    # permission_classes = [permissions.IsAuthenticated]
# 
    def perform_create(self, serializer):
        user = serializer.save()

# Filtrage pour les posts
class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')  # Filtrer par titre de post

    class Meta:
        model = Post
        fields = ['title']  # Ajoutez d'autres champs que vous souhaitez filtrer

# ViewSet pour les posts
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = CustomPagination
    filterset_class = PostFilter  # Utilisation de la classe de filtre

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
