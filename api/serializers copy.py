# api/serializers.py

from myUser.models import Profile
from rest_framework import serializers

from posts.models import Message, Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'profile_picture', 'bio']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()  # Sérialiseur imbriqué pour le profil
    posts = serializers.PrimaryKeyRelatedField(many=True, read_only=True)  # Liens vers les posts

    class Meta:
        model = User
        fields = ['id', 'email', 'profile', 'posts']

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Détails de l'utilisateur qui a commenté

    class Meta:
        model = Comment
        fields = ['id', 'post', 'user', 'content', 'created_at']

class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # Détails de l'utilisateur qui a créé le post
    comments = CommentSerializer(many=True, read_only=True)  # Sérialiseur imbriqué pour les commentaires

    class Meta:
        model = Post
        fields = ['id', 'user', 'content', 'image', 'created_at', 'comments']  

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)  # Détails de l'utilisateur qui a envoyé le message
    receiver = UserSerializer(read_only=True)  # Détails de l'utilisateur qui a reçu le message

    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'content', 'created_at']        




# Liste des utilisateurs : http://127.0.0.1:8000/api/users/
# Liste des posts : http://127.0.0.1:8000/api/posts/
# Liste des commentaires : http://127.0.0.1:8000/api/comments/
# Liste des messages : http://127.0.0.1:8000/api/messages/        