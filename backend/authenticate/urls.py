from django.urls import path
from .views import (
    login,
    signup,
    logout
)

urlpatterns = [
    path('login', login, name='Login'),
    path('login', login, name='Login'),
    path('login', login, name='Login'),
]
