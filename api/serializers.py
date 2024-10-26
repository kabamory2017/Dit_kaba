# api/serializers.py

from myUser.models import MyUser, Profile
from myUser.utils import send_activation_email
from rest_framework import serializers

from posts.models import Message, Post, Comment
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
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


class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'email', 'password')  # Champs à inclure
        extra_kwargs = {'password': {'write_only': True}}  # Mot de passe uniquement en écriture

    def create(self, validated_data):
        user = MyUser(
            email=validated_data['email'],
            
        )
        user.set_password(validated_data['password'])  # Hacher le mot de passe
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email  # Ajoutez des informations supplémentaires au token
        return token

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email is None or password is None:
            raise serializers.ValidationError(
                'Les champs "email" et "password" sont requis.'
            )

        try:
            user = MyUser.objects.get(email=email)  # Utilisez votre modèle personnalisé
        except MyUser.DoesNotExist:
            raise serializers.ValidationError('L\'utilisateur avec cet email n\'existe pas.')

        if not user.check_password(password):
            raise serializers.ValidationError('Le mot de passe est incorrect.')

        attrs['user'] = user
        user_data = MyUserSerializer(user).data
        return {**super().validate(attrs), 'user': user_data} 

# Liste des utilisateurs : http://127.0.0.1:8000/api/users/
# Liste des posts : http://127.0.0.1:8000/api/posts/
# Liste des commentaires : http://127.0.0.1:8000/api/comments/
# Liste des messages : http://127.0.0.1:8000/api/messages/        

class ActivationTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('email',)

    def create(self, validated_data):
        user = MyUser.objects.create(**validated_data)
        # Créez un token d'activation
        token = RefreshToken.for_user(user)
        # Envoyez l'e-mail d'activation avec le token
        send_activation_email(user.email, user)  # Vous aurez besoin de cette fonction
        return user