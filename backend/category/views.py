from django.http import JsonResponse
from products.models import Product

def product_list(request):
    products = products.Product.objects.all()
    product_list = list(products.values('product_id', 'product_name', 'product_description', 'product_price'))  # Adjust the fields as needed
    return JsonResponse({'products': product_list})
