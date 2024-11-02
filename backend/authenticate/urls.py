from django.urls import path
from .views import (
    login,
    signup,
    logout
)

urlpatterns = [
    path('', login,name='login'),
    path('signup',signup,name='signup'),
    path('logout',logout,name='LogOut')
]
