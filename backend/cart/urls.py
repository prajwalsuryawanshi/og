from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart_api'),
    path('remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart_api'),
    path('', views.view_cart, name='view_cart_api'),
    path('all', views.view_all_carts, name='view_all_cart_api'),
]
