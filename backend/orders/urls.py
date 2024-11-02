from django.urls import path
from .views import place_order 

urlpatterns = [
    path('place',place_order,name='Place_Order')
]
