from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Order
from django.http import JsonResponse
from rest_framework import status
from django.db import transaction
from .models import Order
from customer.models import Customer
from products.models import Product

@api_view(['POST'])
def place_order(request):
    data = request.data

    # Validate required fields
    required_fields = ['customer_id', 'product_id', 'quantity', 'address', 'order_total', 'order_status', 'payment_type']
    for field in required_fields:
        if field not in data:
            return JsonResponse({'error': f'{field} is required'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if customer_id exists
    try:
        customer = Customer.objects.get(customer_id=data['customer_id'])
    except Customer.DoesNotExist:
        return JsonResponse({'error': 'Invalid customer_id'}, status=status.HTTP_400_BAD_REQUEST)

    # Check if product_id exists
    try:
        product = Product.objects.get(product_id=data['product_id'])
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Invalid product_id'}, status=status.HTTP_400_BAD_REQUEST)

    # Create the order within a transaction
    with transaction.atomic():
        new_order = Order.objects.create(
            customer_id=customer,
            product_id=product,
            quantity=data['quantity'],
            address=data['address'],
            order_total=data['order_total'],
            order_status=data['order_status'],
            payment_type=data['payment_type'],
        )

    return JsonResponse({'order_id': new_order.order_id}, status=status.HTTP_201_CREATED)

