# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import UserViewSet, PostViewSet, CommentViewSet, MessageViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'messages', MessageViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Inclure les routes du router
]
