from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from products.serializers import ProductSerializer
from .models import Cart
from customer.models import Customer
from products.models import Product
from .serializers import CartSerializer
from rest_framework import status

@api_view(['POST'])
def add_to_cart(request):
    customer_id = request.query_params.get('customer_id')
    product_id = request.query_params.get('product_id')
    
    if not customer_id or not product_id:
        return Response({'error': 'Both customer_id and product_id are required.'}, status=status.HTTP_400_BAD_REQUEST)

    customer = get_object_or_404(Customer, pk=customer_id)

    product = get_object_or_404(Product, product_id=product_id)

    cart_item, created = Cart.objects.get_or_create(customer_id=customer, product_id=product)

    if not created:
        cart_item.qty += 1
    else:
        cart_item.qty = 1

    cart_item.total = cart_item.qty * product.product_price
    cart_item.save()

    return Response({
        'message': 'Product added to cart successfully',
        'cart_item_qty': cart_item.qty,
        'cart_total': cart_item.total
    })


@api_view(['POST'])
def update_cart(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')
    action = request.data.get('action')  # 'increase', 'decrease', or 'delete'

    if not customer_id or not product_id or not action:
        return Response({'error': 'customer_id, product_id, and action are required.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        cart_item = Cart.objects.get(customer_id_id=customer_id, product_id_id=product_id)

        if action == 'increase':
            cart_item.qty += 1
        elif action == 'decrease':
            if cart_item.qty > 1:
                cart_item.qty -= 1
            else:
                return Response({"message": "Cannot decrease quantity below 1."}, status=status.HTTP_400_BAD_REQUEST)
        elif action == 'delete':
            cart_item.delete()
            return Response({"message": "Item removed from cart."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid action."}, status=status.HTTP_400_BAD_REQUEST)

        cart_item.total = cart_item.qty * cart_item.product_id.product_price  # Update total price
        cart_item.save()

        return Response({"message": "Cart updated successfully", "cart_item_qty": cart_item.qty, "cart_total": cart_item.total}, status=status.HTTP_200_OK)

    except Cart.DoesNotExist:
        return Response({"message": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def view_cart(request):
    customer_id = request.query_params.get('customer_id')

    if not customer_id:
        return Response({"error": "customer_id not provided"}, status=status.HTTP_400_BAD_REQUEST)

    cart_items = Cart.objects.filter(customer_id_id=customer_id).select_related('product_id')

    if not cart_items.exists():
        return Response({"message": "No cart items found."}, status=status.HTTP_404_NOT_FOUND)

    cart_data = []
    total_cost = 0
    total_quantity = 0

    for item in cart_items:
        total_cost += item.total
        total_quantity += item.qty

        cart_item_data = CartSerializer(item).data
        product_data = ProductSerializer(item.product_id).data
        cart_item_data['product'] = product_data
        cart_data.append(cart_item_data)

    return Response({'cart_items': cart_data, 'total_cost': total_cost, 'total_qty': total_quantity})


@api_view(['GET'])
def view_all_carts(request):
    cart_items = Cart.objects.all()

    if not cart_items.exists():
        return Response({"message": "No cart items found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = CartSerializer(cart_items, many=True)
    total_cost = sum(item.total for item in cart_items)

    return Response({'cart_items': serializer.data, 'total_cost': total_cost})
