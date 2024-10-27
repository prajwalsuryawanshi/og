from django.urls import path
from . import views

urlpatterns = [
    path('add', views.add_to_cart, name='add_to_cart_api'),
    path('update', views.update_cart, name='update_cart'),
    path('', views.view_cart, name='view_cart_api'),
    path('all', views.view_all_carts, name='view_all_cart_api'),
]
