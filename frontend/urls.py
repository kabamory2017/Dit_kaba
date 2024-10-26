from atexit import register
from pyexpat import features
from django.urls import path
from .views import contact, home, about, login,register


app_name = 'frontend'
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('register/', register, name='register'),
]
