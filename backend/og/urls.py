from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/' , include('cart.urls') ),
    path('order/' , include('orders.urls') ),
    path('category/' , include('category.urls')),
    path('products/' , include('products.urls')),
    path('customer/' , include('customer.urls')),
    path('payments/',include ('payments.urls'))
]
