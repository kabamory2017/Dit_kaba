# accounts/urls.py
from django.urls import path

from posts.views import PostListView
from .views import UserListView, register, activate,logout_view,CustomPasswordChangeView,follow_user, unfollow_user,all_users,update_profile,follow_user, unfollow_user, profile_view
from . import views

from .forms import CustomAuthenticationForm
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', register, name='register'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
     
      
      # path('profiles/', profile_list, name='profile_list'),
    
    #  path('profiles/', profile_list, name='profile_list'),
   
    #  path('', views.home, name='home'),
     
      path('profile/update/', update_profile, name='update_profile'),
      path('', PostListView.as_view(), name='post_list'),

    #  path('login/', auth_views.LoginView.as_view(
    #     template_name='login.html',
    #     authentication_form=CustomAuthenticationForm  # Utilise le formulaire personnalisé
    # ), name='login'),
     path('logout/', logout_view, name='logout'),
     path('login/', views.login_view, name='login'),
      path('change-password/', CustomPasswordChangeView.as_view(), name='change_password'),
         
    # path('unfollow/<int:user_id>/', unfollow_user, name='unfollow_user'),
    path('all-users/', all_users, name='all_users'),

    path('profile/<int:user_id>/', profile_view.as_view(), name='profile'),
    path('follow/<int:user_id>/', follow_user.as_view(), name='follow_user'),
    path('unfollow/<int:user_id>/', unfollow_user.as_view(), name='unfollow_user'),
    path('users/', UserListView.as_view(), name='user_list'),
    
]
