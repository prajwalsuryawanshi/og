from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Customer
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import Customer
from orders.models import Order
from products.models import Product
from products.views import get_wishlist_products

def get_customer_profile(request):
    customer_id = request.GET.get('customer_id')
    if not customer_id:
        return JsonResponse({"error": "Customer ID is required"}, status=400)
    
    # Retrieve the customer object
    customer = get_object_or_404(Customer, customer_id=customer_id)
    
    # Fetch all orders where order_status is 'Delivered'
    previous_orders = Order.objects.filter(customer_id=customer_id, order_status="Delivered")
    
    customer_data = {
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone_no": customer.phone_no,
        "address": {
            "location": customer.address.location if customer.address else None,
            "city": customer.address.city if customer.address else None,
            "state": customer.address.state if customer.address else None,
            "postal_code": customer.address.pincode if customer.address else None,
        },
        "previous_orders": [],
        "wishlist": get_wishlist_products(customer_id),
    }

    # Iterate through the previous orders and collect the related product information
    for order in previous_orders:
        product = Product.objects.get(product_id=order.product_id.product_id)  # Use product_id from the order
        product_info = {
            "product_id": product.product_id,
            "name": product.product_name,
            "description": product.product_description,
            "price": product.product_price,
            "image": product.product_images,
            "quantity": order.quantity,
            "status": order.order_status
        }
        customer_data["previous_orders"].append(product_info)
    
    return JsonResponse(customer_data)



@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    # Log the received email and password
    print(f"Email: {email}")
    print(f"Password: {password}")

    # Authenticate the customer
    customer = Customer.objects.filter(email=email, password=password).first()

    if customer:
        # Successful authentication
        return Response({"message": "Login successful", "customer_id": customer.customer_id, "name": customer.name}, status=status.HTTP_200_OK)
    else:
        # Authentication failed
        return Response({"error": "Invalid email or password"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def signup(request):
    name = request.data.get('name')
    email = request.data.get('email')
    password = request.data.get('password')
    phone_no = request.data.get('phone_no')

    # Log the received data
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Password: {password}")
    print(f"Phone Number: {phone_no}")

    # Check if the email already exists in the Customer table
    if Customer.objects.filter(email=email).exists():
        return Response({"error": "Email already in use"}, status=status.HTTP_400_BAD_REQUEST)

    # Create a new customer
    try:
        customer = Customer(
            name=name,
            email=email,
            password=password,
            phone_no=phone_no,
            address=None  # Set to None or a default if desired
        )
        customer.save()

        return Response({"message": f"Customer created successfully. Welcome, {name}!"}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": "An error occurred during signup."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def logout(request):
    return render('<h1> Logout </h1>')
