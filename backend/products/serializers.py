from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'product_id',
            'product_name',
            'product_description',
            'product_images',
            'category',
            'product_price',
            'stock_quantity',
            'created_at',
            'updated_at'
        ]
