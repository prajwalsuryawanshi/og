from rest_framework import serializers
from .models import Customer, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['street', 'city', 'state', 'postal_code', 'country']

class CustomerSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Customer
        fields = ['customer_id', 'name', 'email', 'phone_no', 'address', 'created_at', 'updated_at','password']
