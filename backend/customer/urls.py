# urls.py
from django.urls import path
from .views import get_customer_profile,login,signup,logout

urlpatterns = [
    path('profile', get_customer_profile, name='get_customer_profile'),
    path('login', login,name='login'),
    path('signup',signup,name='signup'),
    path('logout',logout,name='LogOut')
]
