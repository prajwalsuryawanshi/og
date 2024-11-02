from rest_framework import serializers
from .models import Order

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model =Order
        fields = [
            'order_id',
            'customer_id',
            'product_id',
            'quantity',
            'address',
            'order_total',
            'order_status',
            'payment_type',
            'created_at',
            'updated_at'
        ]
