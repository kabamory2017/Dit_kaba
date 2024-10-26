# utils.py
from django.core.mail import send_mail
from django.core.mail import BadHeaderError
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken
from django.conf import settings

def send_welcome_email(user):
    subject = _('Bienvenue sur notre plateforme!')
    message = f'Bonjour {user.email},\n\nMerci de vous être inscrit sur notre plateforme. Nous sommes ravis de vous accueillir!'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [user.email]

    try:
        send_mail(subject, message, from_email, recipient_list)
    except BadHeaderError:
        # Gérer l'erreur si nécessaire
        print("Erreur lors de l'envoi de l'e-mail.")

# utils.py


def send_activation_email(email, user):
    token = AccessToken.for_user(user)  # Utilisez AccessToken pour créer un token
    subject = 'Activez votre compte'
    message = f'Pour activer votre compte, cliquez sur le lien suivant : http://127.0.0.1:8000/api/activate/{token}/'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)
