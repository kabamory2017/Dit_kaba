# api/viewsets.py

from myUser.models import MyUser
from posts.models import Comment, Message, Post
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import UserSerializer, PostSerializer, CommentSerializer, MessageSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, TokenError



User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]  # Exiger que l'utilisateur soit authentifié

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Exiger que l'utilisateur soit authentifié

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Exiger que l'utilisateur soit authentifié

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]  # Exiger que l'utilisateur soit authentifié

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class ActivateAccountView(APIView):
    def get(self, request, token):
        try:
            # Validez le token
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Utilisez 'user_id' pour obtenir l'ID utilisateur
            my_user = MyUser.objects.get(id=user_id)  # Récupérez l'utilisateur par ID
            my_user.is_active = True  # Activez l'utilisateur
            my_user.save()
            return Response({"message": "Votre compte a été activé avec succès!"}, status=status.HTTP_200_OK)
        except (TokenError, MyUser.DoesNotExist):
            return Response({"error": "Token invalide ou utilisateur non trouvé."}, status=status.HTTP_400_BAD_REQUEST)  