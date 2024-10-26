# posts/urls.py
from django.urls import path
from .views import MessageDeleteView, NotificationDeleteView, PostListView, PostCreateView, PostDetailView, CommentCreateView, LikeDislikeToggleView,CommentDeleteView,PostDeleteView,PostUpdateView,NotificationListView, post_search,read_notification,NotificationDetailView,SendMessageView,InboxView, user_search

app_name = 'posts'

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    
    path('create/', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('<int:post_id>/comment/', CommentCreateView.as_view(), name='comment_create'),
    path('post/<int:post_id>/like_dislike/', LikeDislikeToggleView.as_view(), name='like_dislike_toggle'),
     path('comment/<int:comment_id>/delete/', CommentDeleteView.as_view(), name='comment_delete'),  # Nouvelle URL
       path('<int:pk>/edit/', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete'),
     path('notifications/', NotificationListView.as_view(), name='notification_list'),
    path('notifications/read/<int:pk>/', read_notification, name='read_notification'),
    path('notifications/<int:pk>/', NotificationDetailView.as_view(), name='notification_detail'),
     path('send/', SendMessageView.as_view(), name='send_message'),
    path('inbox/', InboxView.as_view(), name='inbox'),
     path('notifications/delete/<int:pk>/', NotificationDeleteView.as_view(), name='delete_notification'),
      path('messages/delete/<int:pk>/', MessageDeleteView.as_view(), name='delete_message'),
      path('user/search/', user_search, name='user_search'),
    path('post/search/', post_search, name='post_search'),
]
