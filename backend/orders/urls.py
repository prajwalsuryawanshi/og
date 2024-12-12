from django.urls import path
from .views import PlaceOrderView

urlpatterns = [
    path('',PlaceOrderView.as_view(),name='all_orders')
]
