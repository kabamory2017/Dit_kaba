# posts/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
         return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'post {self.post.content}'

class LikeDislike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes_dislikes')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_like = models.BooleanField()
    
    class Meta:
        unique_together = ['post', 'user']
    
    def __str__(self):
        return f"{'Like' if self.is_like else 'Dislike'} by {self.user.email}"


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Le destinataire de la notification
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)  # Le post associé à la notification
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)  # Le commentaire associé à la notification
    message = models.CharField(max_length=255)  # Le message de la notification
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)  # Pour marquer la notification comme lue

    def __str__(self):
        return f'Notification for {self.user.email}: {self.message}'
    

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from {self.sender} to {self.receiver} at {self.created_at}'