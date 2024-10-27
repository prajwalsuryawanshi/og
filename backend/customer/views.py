from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Customer

def get_customer_profile(request):
    customer_id = request.GET.get('customer_id')
    if not customer_id:
        return JsonResponse({"error": "Customer ID is required"}, status=400)
    
    customer = get_object_or_404(Customer, customer_id=customer_id)
    customer_data = {
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone_no": customer.phone_no,
        "address": {
            "street": customer.address.street if customer.address else None,
            "city": customer.address.city if customer.address else None,
            "state": customer.address.state if customer.address else None,
            "country": customer.address.country if customer.address else None,
            "postal_code": customer.address.postal_code if customer.address else None,
        },
        "created_at": customer.created_at,
        "updated_at": customer.updated_at,
    }
    return JsonResponse(customer_data)
