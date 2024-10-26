from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Comment, LikeDislike, Notification,Message

@receiver(post_save, sender=Comment)
def send_comment_notification(sender, instance, created, **kwargs):
    if created:
        post_author = instance.post.user
        comment_author = instance.user
        if post_author != comment_author:  # Ne pas notifier l'utilisateur si c'est lui-même qui commente
            Notification.objects.create(
                user=post_author,
                post=instance.post,
                comment=instance,  # Référence au commentaire
                message=f"{comment_author.email} a commenté votre post : \"{instance.content}\"."  # Inclut le contenu du commentaire
            )

@receiver(post_save, sender=Message)
def send_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        # Créez une notification pour le destinataire
        Notification.objects.create(
            user=instance.receiver,
            message=f'Vous avez reçu un nouveau message de {instance.sender.email}: "{instance.content}"',
            post=None  # Aucun post associé dans ce cas
        )


@receiver(post_save, sender=LikeDislike)
def send_like_notification(sender, instance, created, **kwargs):
    if created and instance.is_like:  # Vérifie si c'est un nouveau like
        post_author = instance.post.user
        liker = instance.user
        if post_author != liker:  # Ne pas notifier l'auteur du post
            Notification.objects.create(
                user=post_author,
                post=instance.post,
                message=f"{liker.email} a aimé votre post."
            )        