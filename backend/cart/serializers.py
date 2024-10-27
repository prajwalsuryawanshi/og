from rest_framework import serializers
from .models import Cart

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ['id', 'customer_id', 'product_id', 'qty', 'total']  # Include fields you want to expose

    def create(self, validated_data):
        """Create a new cart item."""
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """Update an existing cart item."""
        instance.qty = validated_data.get('qty', instance.qty)
        instance.total = validated_data.get('total', instance.total)
        instance.save()
        return instance
