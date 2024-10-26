# accounts/views.py
from django.shortcuts import render, redirect
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import ListView,DeleteView,DetailView
from django.http import HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages  # Importez le module de messages

from posts.models import Notification
from .forms import ProfileForm,MyUserCreationForm,CustomPasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404, redirect
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from .models import  Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomAuthenticationForm
from django.contrib.auth.views import PasswordChangeView
from django.conf import settings
from django.contrib.auth import logout
from .models import Profile,MyUser

User = settings.AUTH_USER_MODEL
def register(request):
    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True  # L'utilisateur doit activer son compte
            user.save()

            # Envoi de l'email de vérification
            mail_subject = 'Activer votre compte.'
            message = render_to_string('activation_email.html', {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(mail_subject, message)

            messages.success(request, 'Veuillez vérifier votre email pour activer votre compte.')
            return redirect('login')  # Rediriger vers la page de connexion après l'inscription
    else:
        form = MyUserCreationForm()

    return render(request, 'frontend/register.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Votre compte a été activé avec succès.')
        return redirect('post_list')
    else:
        messages.error(request, 'Le lien d\'activation est invalide.')
        return redirect('login')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'Connexion réussie !')  # Message de succès
            return redirect('posts:post_list')  # Rediriger vers la page d'accueil
        else:
            messages.error(request, 'Identifiants invalides. Veuillez réessayer.')  # Message d'erreur
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'frontend/login.html', {'form': form})



# def profile_view(request, user_id):
#     user_profile = get_object_or_404(MyUser, id=user_id).profile
#     is_following = user_profile in request.user.profile.followers.all()
#      # Vérifie si l'utilisateur actuel suit cet utilisateur
#     return render(request, 'frontend/profile.html', {'profile': user_profile, 'is_following': is_following})


class profile_view(DetailView):
    model = MyUser
    template_name = 'frontend/profile.html'
    context_object_name = 'user_profile'

    def get_object(self):
        # Récupérer l'utilisateur en fonction de l'ID passé dans l'URL
        return get_object_or_404(MyUser, id=self.kwargs['user_id'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = self.get_object().profile  # Récupération du profil de l'utilisateur

        # Vérifier si l'utilisateur actuel suit le profil affiché
        if self.request.user.is_authenticated:
            context['is_following'] = user_profile in self.request.user.profile.followers.all()
        else:
            context['is_following'] = False  # Les utilisateurs non connectés ne peuvent pas suivre

        context['profile'] = user_profile  # Ajoutez le profil au contexte

        return context



# @login_required
# def follow_user(request, user_id):
#     user_to_follow = get_object_or_404(MyUser, id=user_id)
#     profile = request.user.profile

#     # Vérifie que l'utilisateur ne peut pas se suivre lui-même
#     if profile.user == user_to_follow:
#         return HttpResponseForbidden("You cannot follow yourself.")

#     # Ajoute l'utilisateur à la liste des followers
#     if user_to_follow.profile not in profile.followers.all():
#         profile.followers.add(user_to_follow.profile)

#         # Crée une notification pour l'utilisateur suivi
#         message = f"{request.user.email} vous suit maintenant."
#         Notification.objects.create(user=user_to_follow, message=message)

#     return redirect('profile', user_id=user_id)

class follow_user(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_follow = get_object_or_404(MyUser, id=user_id)
        profile = request.user.profile

        # Vérifie que l'utilisateur ne peut pas se suivre lui-même
        if profile.user == user_to_follow:
            return HttpResponseForbidden("You cannot follow yourself.")

        # Ajoute l'utilisateur à la liste des followers
        if user_to_follow.profile not in profile.followers.all():
            profile.followers.add(user_to_follow.profile)

            # Crée une notification pour l'utilisateur suivi
            message = f"{request.user.email} vous suit maintenant."
            Notification.objects.create(user=user_to_follow, message=message)

        return redirect('profile', user_id=user_id)


class unfollow_user(LoginRequiredMixin, View):
    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(MyUser, id=user_id)
        profile = request.user.profile

        # Retire l'utilisateur de la liste des followers
        if user_to_unfollow.profile in profile.followers.all():
            profile.followers.remove(user_to_unfollow.profile)

        return redirect('profile', user_id=user_id)




# @login_required
# def unfollow_user(request, user_id):
#     user_to_unfollow = get_object_or_404(MyUser, id=user_id)
#     profile = request.user.profile

#     # Retire l'utilisateur de la liste des followers
#     if user_to_unfollow.profile in profile.followers.all():
#         profile.followers.remove(user_to_unfollow.profile)

#     return redirect('profile', user_id=user_id)

@login_required
def update_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = ProfileForm(instance=profile)
    
    return render(request, 'frontend/update_profile.html', {'form': form})  

def home(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    return redirect('login')

class CustomPasswordChangeView(PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'frontend/change_password.html'
    success_url = '/'

def all_users(request):
    users = MyUser.objects.all()  # Liste de tous les utilisateurs
    return render(request, 'frontend/all_users.html', {'users': users})    

class UserListView(ListView):
    model = Profile
    template_name = 'frontend/user_list.html'  # Template à utiliser
    context_object_name = 'profiles'
    paginate_by = 10  # Nombre d'utilisateurs à afficher par page (optionnel)

    def get_queryset(self):
        # Vous pouvez trier les profils si nécessaire, par exemple par date de création
        return Profile.objects.all().order_by('user__email')
    
class PublicProfileView(DetailView):
    model = Profile
    template_name = 'frontend/public_profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Récupérer le profil correspondant au nom d'utilisateur passé dans l'URL
        return get_object_or_404(Profile, user__username=self.kwargs['username'])    