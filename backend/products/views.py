from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from products.models import Product
import json
from django.shortcuts import render

def template_test(request):
    context ={
        'name': 'Aditya'
    } 
    return render(request, 'index.html',context)

# Function to list all products
def product_list(request):
    products = Product.objects.all()
    product_list = list(products.values('product_id', 'product_name', 'product_description', 'product_price'))
    return JsonResponse({'products': product_list})


@csrf_exempt
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

def filter_products(request):
    products = Product.objects.all()

    # Get filter criteria from query parameters
    product_name = request.GET.get('product_name', None)
    category_id = request.GET.get('category_id', None)
    min_price = request.GET.get('min_price', None)
    max_price = request.GET.get('max_price', None)
    
    # Apply filters based on provided criteria
    if product_name:
        products = products.filter(product_name__icontains=product_name)
    if category_id:
        products = products.filter(category_id=category_id)
    if min_price:
        products = products.filter(product_price__gte=min_price)
    if max_price:
        products = products.filter(product_price__lte=max_price)

    # Convert the queryset to a list of dictionaries
    product_list = list(products.values('product_id', 'product_name', 'product_description', 'product_price'))
    
    return JsonResponse({'products': product_list})

