from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Cart
from products.models import Product

@api_view(['POST'])
def add_to_cart(request, product_id):
    customer_id = request.user.id  # Get the logged-in user

    try:
        # Retrieve the product instance using the correct field name
        product = Product.objects.get(product_id=product_id)  # Assuming product_id is the correct field
    except Product.DoesNotExist:
        return Response({'message': 'Product not found'}, status=404)

    # Create or update the cart item using the Product instance
    cart_item, created = Cart.objects.get_or_create(customer_id=customer_id, product_id=product_id)  # Use product instance

    if not created:
        # If the item is already in the cart, increase the quantity
        cart_item.qty += 1
    else:
        # Set initial quantity to 1 if it is newly added to the cart
        cart_item.qty = 1

    # Calculate the total price based on quantity
    cart_item.total = cart_item.qty * product.product_price  # Use product.product_price
    cart_item.save()

    return Response({'message': 'Product added to cart successfully', 'cart_item_qty': cart_item.qty})



@api_view(['POST'])
def remove_from_cart(request, product_id):
    customer_id = request.user.id
    try:
        cart_item = Cart.objects.get(customer_id=customer_id, product_id=product_id)
        
        if cart_item.qty > 1:
            # Decrease the quantity
            cart_item.qty -= 1
            cart_item.total = cart_item.qty * cart_item.product.price
            cart_item.save()
        else:
            # Remove item if quantity is 1
            cart_item.delete()
        
        return Response({'message': 'Product removed from cart', 'cart_item_qty': cart_item.qty})
    
    except Cart.DoesNotExist:
        return Response({'error': 'Product not found in the cart'}, status=404)
    

@api_view(['GET'])
def view_cart(request):
    # Get customer_id from query parameters
    customer_id = request.query_params.get('customer_id')

    if not customer_id:
        return Response({"error": "customer_id not provided"}, status=400)
    
    print(f"Received customer_id: {customer_id}")

    # Filter the Cart based on customer_id
    cart_items = Cart.objects.filter(customer_id=customer_id)

    if not cart_items.exists():
        print("No cart items found for this customer_id.")
    
    # Prepare a response with cart details
    cart_data = []
    total_cost = 0
    for item in cart_items:
        total_cost += item.total
        cart_data.append({
            'product_name': item.product.product_name,
            'product_price': item.product.product_price,
            'quantity': item.qty,
            'total': item.total
        })

    return Response({'cart_items': cart_data, 'total_cost': total_cost})

@api_view(['GET'])
def view_all_carts(request):
    # Retrieve all cart items
    cart_items = Cart.objects.all()

    if not cart_items.exists():
        print("No cart items found.")
    
    # Prepare a response with cart details
    cart_data = []
    total_cost = 0
    for item in cart_items:
        total_cost += item.total
        cart_data.append({
            'customer_id': item.customer_id,  # Include customer_id if needed
            'product_name': item.product.product_name,
            'product_price': item.product.product_price,
            'quantity': item.qty,
            'total': item.total
        })

    return Response({'cart_items': cart_data, 'total_cost': total_cost})
