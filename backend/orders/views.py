from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Order, OrderItem
from customer.models import Customer, Address
from products.models import Product
from django.db import transaction

class PlaceOrderView(APIView):
    def post(self, request):
        data = request.data

        # Extract order-level details
        customer_id = data.get('customer_id')
        address_id = data.get('address_id')
        payment_type = data.get('payment_type')
        order_items = data.get('order_items')  # List of {"product_id": X, "quantity": Y}

        if not all([customer_id, payment_type, order_items]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Invalid customer ID."}, status=status.HTTP_404_NOT_FOUND)

        if address_id:
            try:
                address = Address.objects.get(id=address_id)
            except Address.DoesNotExist:
                return Response({"error": "Invalid address ID."}, status=status.HTTP_404_NOT_FOUND)
        else:
            address = None

        with transaction.atomic():
            # Create the order
            order = Order.objects.create(
                customer_id=customer,
                address_id=address,
                order_total=0,  # Will calculate this based on order items
                order_status="Pending",
                payment_type=payment_type
            )

            total = 0
            for item in order_items:
                product_id = item.get('product_id')
                quantity = item.get('quantity')

                if not all([product_id, quantity]):
                    return Response({"error": "Each order item must have a product_id and quantity."}, status=status.HTTP_400_BAD_REQUEST)

                try:
                    product = Product.objects.get(id=product_id)
                except Product.DoesNotExist:
                    return Response({"error": f"Invalid product ID {product_id}."}, status=status.HTTP_404_NOT_FOUND)

                if quantity <= 0:
                    return Response({"error": "Quantity must be a positive integer."}, status=status.HTTP_400_BAD_REQUEST)

                # Create the order item
                OrderItem.objects.create(order=order, product=product, quantity=quantity)

                # Add to total
                total += product.price * quantity

            # Update the order total
            order.order_total = total
            order.save()

        return Response({"message": "Order placed successfully.", "order_id": order.order_id}, status=status.HTTP_201_CREATED)
