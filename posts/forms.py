# posts/forms.py

from django import forms
from .models import Post, Comment,Message
from django.contrib.auth import get_user_model

User = get_user_model()



class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title',  'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'content']
    
    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)  # Extraire le sender des kwargs
        super().__init__(*args, **kwargs)
        if sender:
            # Exclure l'expéditeur de la liste des destinataires
            self.fields['receiver'].queryset = User.objects.exclude(id=sender.id)
        else:
            self.fields['receiver'].queryset = User.objects.all()  # Si p


class UserSearchForm(forms.Form):
    query = forms.CharField(label='Recherche d\'utilisateurs', max_length=100)            

class PostSearchForm(forms.Form):
    query = forms.CharField(label='Recherche de posts', max_length=255, required=False)  # Champ pour le contenu
    date_from = forms.DateField(label='Date à partir de', required=False)  # Champ pour la date de début
    date_to = forms.DateField(label='Date jusqu\'à', required=False)  # Champ pour la date de fin