from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .models import Product,Review
from customer.models import Customer
import json
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404

# Function to list all products
@api_view(['GET'])
def product_list(request):
    products = Product.objects.select_related('category').all()
    # Create a list with custom field names, including category_name
    product_list = [
        {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_description': product.product_description,
            'product_price': product.product_price,
            'stock_quantity': product.stock_quantity,
            'category_name': product.category.category_name  # Accessing the related category's name
        }
        for product in products
    ]
    
    return JsonResponse({'products': product_list})

@csrf_exempt
@api_view(['POST'])
def add_product(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Handle product_images, default to an empty array if not provided or empty
        product_images = data.get('product_images', [])
        if not product_images:  # If product_images is an empty string or empty list
            product_images = '{}'

        new_product = Product.objects.create(
            product_name=data['product_name'],
            product_description=data['product_description'],
            product_images=product_images,  # Ensure valid array format
            category_id=data['category_id'],
            product_price=data['product_price'],
            stock_quantity=data['stock_quantity']
        )
        return JsonResponse({'product_id': new_product.product_id}, status=201)

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Function to update a product's information
@api_view(['POST'])
@csrf_exempt
def update_product(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

    if request.method == 'PUT':
        data = json.loads(request.body)

        product.product_name = data.get('product_name', product.product_name)
        product.product_description = data.get('product_description', product.product_description)

        # Handle product_images as a list (assuming multiple images are passed)
        product_images = data.get('product_images', product.product_images)
        if isinstance(product_images, list):
            # Handle it if it's a list (assuming it's an array field in your DB)
            product.product_images = product_images

        product.product_price = data.get('product_price', product.product_price)
        product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
        product.save()

        return JsonResponse({'message': 'Product updated successfully'})

    return JsonResponse({'error': 'Invalid request method'}, status=400)

# Function to delete a product
@csrf_exempt
def delete_product(request, product_id):
    try:
        product = Product.objects.get(product_id=product_id)
        product.delete()
        return JsonResponse({'message': 'Product deleted successfully'}, status=204)
    except Product.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)

@api_view(['GET'])
def filter_products(request):
    products = Product.objects.select_related('category').all()

    # Get filter criteria from query parameters
    product_name = request.GET.get('product_name', None)
    category_id = request.GET.get('category_id', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    print('Product Name:', product_name, 'Category ID:', category_id, 'Min Price:', min_price, 'Max Price:', max_price)
    
    # Apply filters based on provided criteria
    if product_name:
        products = products.filter(product_name__icontains=product_name)
    if category_id:
        products = products.filter(category_id=category_id)
    if min_price:
        products = products.filter(product_price__gte=min_price)
    if max_price:
        products = products.filter(product_price__lte=max_price)

    # Use list comprehension to create the product list with direct attribute access
    product_list = [
        {
            'product_id': product.product_id,
            'product_name': product.product_name,
            'product_description': product.product_description,
            'product_price': product.product_price,
            'stock_quantity': product.stock_quantity,
            'category_name': product.category.category_name  # Accessing the related category's name
        }
        for product in products
    ]

    return JsonResponse({'products': product_list})

@csrf_exempt
@api_view(['POST'])
def add_review(request):
    # Extract data from the request body
    product_id = request.data.get('product_id')
    customer_id = request.data.get('customer_id')
    rating = request.data.get('rating')
    review_text = request.data.get('review_text')
    
    # Validate data (make sure the necessary fields are provided)
    if not product_id or not customer_id or not rating or not review_text:
        return JsonResponse({"error": "All fields are required."}, status=400)

    try:
        # Check if the product and customer exist in the database
        product = Product.objects.get(product_id=product_id)
        customer = Customer.objects.get(customer_id=customer_id)

        # Validate the rating (should be an integer between 1 and 5)
        if not (1 <= rating <= 5):
            return JsonResponse({"error": "Rating must be between 1 and 5."}, status=400)

        # Create the review
        review = Review.objects.create(
            product_id=product,
            customer_id=customer,
            rating=rating,
            review_text=review_text
        )

        # Return success response with created review data
        return JsonResponse({
            "message": "Review added successfully.",
            "review_id": review.review_id,
            "product_id": product.product_id,
            "rating": review.rating,
            "review_text": review.review_text
        }, status=201)

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found."}, status=404)
    
    except Customer.DoesNotExist:
        return JsonResponse({"error": "Customer not found."}, status=404)
    
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@api_view(['GET'])
def get_reviews(request):
    product_id = request.GET.get('product_id')
    
    # Check if product_id is provided
    if not product_id:
        return JsonResponse({'error': 'Product ID is required.'}, status=400)

    try:
        # Get all reviews for the specified product
        reviews = Review.objects.filter(product_id=product_id)
        
        # Calculate the average rating
        total_rating = sum(review.rating for review in reviews)
        average_rating = total_rating / reviews.count() if reviews.exists() else 0
        
        # Prepare the list of reviews
        review_list = [
            {
                'review_id': review.review_id,
                'customer_id': review.customer_id.customer_id,
                'rating': review.rating,
                'review': review.review_text,
                'created_at': review.created_at,
                'updated_at': review.updated_at
            }
            for review in reviews
        ]
        
        # Return response with reviews and average rating
        return JsonResponse({
            'reviews': review_list,
            'average_rating': round(average_rating, 2)
        }, status=200)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@api_view(['DELETE'])
def delete_review(request):
    review_id=request.GET.get('review_id')
    try:
        # Attempt to retrieve the review by its ID
        review = Review.objects.get(review_id=review_id)
        
        # Delete the review
        review.delete()
        
        return JsonResponse({'message': 'Review deleted successfully'}, status=200)

    except Review.DoesNotExist:
        # If the review with the given ID does not exist
        return JsonResponse({'error': 'Review not found'}, status=404)

    except Exception as e:
        # Handle any other unexpected exceptions
        return JsonResponse({'error': str(e)}, status=500)

@api_view(['POST'])
def add_to_wishlist(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')

    # Check if customer_id and product_id are provided
    if not customer_id or not product_id:
        return JsonResponse({"error": "Customer ID and Product ID are required"}, status=400)

    # Retrieve the customer object
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Check if the product exists
    product = get_object_or_404(Product, product_id=product_id)

    # Add the product_id to the wishlist if not already present
    if product_id not in customer.wishlist:
        customer.wishlist.append(product_id)
        customer.save()
        return JsonResponse({"message": f"Product {product_id} added to wishlist"}, status=201)
    else:
        return JsonResponse({"message": f"Product {product_id} is already in the wishlist"}, status=200)
    
@api_view(['POST'])
def remove_from_wishlist(request):
    customer_id = request.data.get('customer_id')
    product_id = request.data.get('product_id')

    # Check if customer_id and product_id are provided
    if not customer_id or not product_id:
        return JsonResponse({"error": "Customer ID and Product ID are required"}, status=400)

    # Retrieve the customer object
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Ensure customer.wishlist is an initialized list
    if customer.wishlist is None:
        return JsonResponse({"error": "Wishlist is empty"}, status=400)

    # Check if the product is in the wishlist
    if product_id in customer.wishlist:
        customer.wishlist.remove(product_id)
        customer.save()
        return JsonResponse({"message": f"Product {product_id} removed from wishlist"}, status=200)
    else:
        return JsonResponse({"message": f"Product {product_id} not found in the wishlist"}, status=404)
    
from products.models import Product

def get_wishlist_products(customer_id):
    customer = get_object_or_404(Customer, customer_id=customer_id)

    # Check if the wishlist is not empty
    if not customer.wishlist:
        return []

    # Retrieve products based on wishlist product IDs
    products = Product.objects.filter(product_id__in=customer.wishlist)
    wishlist_products = []

    for product in products:
        product_info = {
            "product_id": product.product_id,
            "name": product.product_name,
            "description": product.product_description,
            "price": product.product_price,
            "image": product.product_images
        }
        wishlist_products.append(product_info)
    
    return wishlist_products

