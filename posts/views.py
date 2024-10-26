# posts/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, DetailView
from .models import Post, Comment,LikeDislike,Message
from .forms import MessageForm, PostForm, CommentForm, PostSearchForm, UserSearchForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Notification
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()


class PostListView(ListView):
    model = Post
    template_name = 'frontend/post_list.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Compter les notifications non lues
        # context['unread_notifications_count'] = self.request.user.notifications.filter(is_read=False).count()
        # context['unread_notifications_count'] = self.request.user.notification_set.filter(is_read=False).count()

        # Ajouter le comptage des likes, dislikes et commentaires pour chaque post
        for post in context['posts']:
            post.likes_count = post.likes_dislikes.filter(is_like=True).count()
            post.dislikes_count = post.likes_dislikes.filter(is_like=False).count()
            post.comments_count = post.comments.count()

        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'frontend/post_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_list')
    
class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'frontend/post_update.html'

    # Assure-toi que seul l'utilisateur qui a créé le post puisse le modifier
    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.user != self.request.user:
            raise PermissionDenied
        return post

    def get_success_url(self):
        return reverse_lazy('posts:post_detail', kwargs={'pk': self.object.pk})    
    
class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'frontend/post_confirm_delete.html'

    # Assure-toi que seul l'utilisateur qui a créé le post puisse le supprimer
    def get_object(self):
        post = get_object_or_404(Post, id=self.kwargs['pk'])
        if post.user != self.request.user:
            raise PermissionDenied
        return post

    def get_success_url(self):
        return reverse_lazy('posts:post_list')    

class PostDetailView(DetailView):
    model = Post
    template_name = 'frontend/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Calculer le nombre de likes et dislikes
        context['likes_count'] = self.object.likes_dislikes.filter(is_like=True).count()
        context['dislikes_count'] = self.object.likes_dislikes.filter(is_like=False).count()
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        context['comment_form'] = CommentForm()

        # Vérifier si l'utilisateur est authentifié pour gérer likes/dislikes
        if self.request.user.is_authenticated:
            # Vérifier si l'utilisateur a déjà liké ou disliké le post
            user_like_dislike = self.object.likes_dislikes.filter(user=self.request.user).first()
            if user_like_dislike:
                context['user_liked'] = user_like_dislike.is_like  # True pour like, False pour dislike
            else:
                context['user_liked'] = None  # Aucun like/dislike
        else:
            # Si l'utilisateur n'est pas connecté, on ne peut pas vérifier les likes/dislikes
            context['user_liked'] = None  # Aucun like/dislike pour les utilisateurs non connectés

        return context

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'frontend/comment_form.html'

    def form_valid(self, form):
        post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.user = self.request.user
        form.instance.post = post
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:post_detail', kwargs={'pk': self.kwargs['post_id']})
    
class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, request, comment_id):
        # Récupérer le commentaire à supprimer
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Vérifier que l'utilisateur est bien le propriétaire du commentaire
        if comment.user == request.user:
            comment.delete()  # Supprimer le commentaire
            
        # Rediriger vers la page de détail du post
        return redirect('posts:post_detail', pk=comment.post.id)


# class LikeDislikeToggleView(LoginRequiredMixin, View):
#     def post(self, request, post_id):
#         post = get_object_or_404(Post, id=post_id)
#         user = request.user
#         like_dislike = LikeDislike.objects.filter(post=post, user=user).first()

#         if like_dislike:
#             like_dislike.delete()
#         else:
#             LikeDislike.objects.create(post=post, user=user, is_like=True)  # Pour un like

#         return reverse('posts:post_detail', pk=post.id)    

class LikeDislikeToggleView(LoginRequiredMixin, View):
    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        is_like = request.POST.get('is_like') == 'true'  # On vérifie si l'utilisateur a cliqué sur "Like" ou "Dislike"

        # Chercher s'il y a déjà un "like" ou "dislike" pour ce post par cet utilisateur
        like_dislike = LikeDislike.objects.filter(post=post, user=user).first()

        if like_dislike:
            if like_dislike.is_like != is_like:
                # L'utilisateur a changé son choix : on modifie l'état
                like_dislike.is_like = is_like
                like_dislike.save()
            else:
                # L'utilisateur a déjà fait cette action : on supprime
                like_dislike.delete()
        else:
            # Si l'utilisateur n'a pas encore liké ou disliké, on en crée un nouveau
            LikeDislike.objects.create(post=post, user=user, is_like=is_like)

        # Redirige vers la page de détail du post
        return redirect('posts:post_detail', pk=post.id)
    
class NotificationListView(ListView):
    model = Notification
    template_name = 'frontend/notification_list.html'  # Assurez-vous que le template existe
    context_object_name = 'notifications'
    
    def get_queryset(self):
        # Filtrez les notifications de l'utilisateur connecté
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Compte des notifications non lues
        context['unread_notifications_count'] = self.request.user.notification_set.filter(is_read=False).count()
        
        return context
        
    
def read_notification(request, pk):
    n = get_object_or_404(Notification, pk=pk, user=request.user)
    n.is_read = True
    n.save()
    return redirect('posts:notification_detail', pk=pk)


class NotificationDetailView(DetailView):
    model = Notification
    template_name = 'frontend/notification_detail.html'
    context_object_name = 'notification'

    def get_object(self):
        notification = super().get_object()
        # Marquer la notification comme lue lorsqu'elle est consultée
        if not notification.is_read:
            notification.is_read = True
            notification.save()
        return notification
    
class NotificationDeleteView(LoginRequiredMixin, DeleteView):
    model = Notification
    template_name = 'frontend/notification_confirm_delete.html'  # Modèle de confirmation de suppression
    context_object_name = 'notification'
    success_url = reverse_lazy('posts:notification_list')  # URL vers laquelle rediriger après la suppression

    def get_queryset(self):
        # S'assure que l'utilisateur ne peut supprimer que ses propres notifications
        return super().get_queryset().filter(user=self.request.user)



class SendMessageView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'frontend/send_message.html'  # Assurez-vous que le chemin est correct
    success_url = reverse_lazy('posts:inbox')  # Redirige vers la boîte de réception après l'envoi

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['sender'] = self.request.user  # Passer l'utilisateur actuel comme expéditeur
        return kwargs

    def form_valid(self, form):
        form.instance.sender = self.request.user  # Définir l'expéditeur sur le message
        return super().form_valid(form)


# class MessageDeleteView(DeleteView):
#     model = Message
#     template_name = 'posts/message_confirm_delete.html'
#     success_url = reverse_lazy('posts:inbox')

#     def get_object(self, queryset=None):
#         obj = super().get_object(queryset)
#         if obj.sender != self.request.user:
#             raise Http404("Vous n'êtes pas autorisé à supprimer ce message.")
#         return obj


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'frontend/message_confirm_delete.html'
    success_url = reverse_lazy('posts:inbox')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.receiver != self.request.user:  # Vérifie que l'utilisateur est le destinataire
            raise Http404("Vous n'êtes pas autorisé à supprimer ce message.")
        return obj


class InboxView(ListView):
    model = Message
    template_name = 'frontend/inbox.html'
    context_object_name = 'messages'

    def get_queryset(self):
        # Filtrer les messages pour l'utilisateur connecté
        return Message.objects.filter(receiver=self.request.user).order_by('-created_at')    
    
def user_search(request):
    form = UserSearchForm()
    users = []

    if 'query' in request.GET:
        form = UserSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            users = User.objects.filter(pseudo__icontains=query)  # Recherche par pseudo

    return render(request, 'frontend/user_search.html', {'form': form, 'users': users})

def post_search(request):
    form = PostSearchForm()
    posts = Post.objects.none()  # Initialiser avec un queryset vide

    if 'query' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            date_from = form.cleaned_data['date_from']
            date_to = form.cleaned_data['date_to']

            # Filtrer par contenu
            posts = Post.objects.filter(content__icontains=query) if query else Post.objects.all()

            # Filtrer par date si fourni
            if date_from:
                posts = posts.filter(created_at__date__gte=date_from)  # Postes créés à partir de cette date
            if date_to:
                posts = posts.filter(created_at__date__lte=date_to)  # Postes créés jusqu'à cette date

    return render(request, 'frontend/post_search.html', {'form': form, 'posts': posts})