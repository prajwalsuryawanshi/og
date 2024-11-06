from django.urls import path
from .views import (
    product_list,
    add_product,
    update_product,
    delete_product,
    filter_products,
    add_review,
    get_reviews,
    delete_review
)

urlpatterns = [
    path('', product_list, name='product_list'),  # List all products
    path('add/', add_product, name='add_product'),  # Add a new product
    path('update/<int:product_id>/', update_product, name='update_product'),  # Update product info
    path('delete/<int:product_id>/', delete_product, name='delete_product'),  # Delete a product
    path('filter/', filter_products, name='filter_products'),  # Filter products
    path('addreview',add_review,name='addReview'),
    path('getreviews',get_reviews,name= 'getReviews'),
    path('deleteReview',delete_review,name='deleteReview')

]
