from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import MyUser, Profile

# Signal qui est appelé après la création d'un utilisateur
@receiver(post_save, sender=MyUser)
def create_profile(sender, instance, created, **kwargs):
    if created:
        profile= Profile.objects.create(user=instance)
        if not profile.profile_picture:
            profile.profile_picture = 'User_pics/default.jpeg'
        profile.save()
        print(f"Profil créé pour l'utilisateur {instance.email}")
        print(f"Profil créé pour l'utilisateur {instance.email}")

@receiver(post_save, sender=MyUser)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
