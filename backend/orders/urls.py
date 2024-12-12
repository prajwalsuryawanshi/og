from django.urls import path
from .views import place_order 

urlpatterns = [
    path('',place_order,name='all_orders')
]
