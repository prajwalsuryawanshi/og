# urls.py
from django.urls import path
from .views import get_customer_profile

urlpatterns = [
    path('profile/', get_customer_profile, name='get_customer_profile'),
]
