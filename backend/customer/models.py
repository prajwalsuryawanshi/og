from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Address(models.Model):
    address_id = models.AutoField(primary_key=True)
    pincode = models.CharField(max_length=10)  # Adjust length based on your needs
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    location = models.CharField(max_length=255)  # Specific or descriptive location details
    landmark = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location}, {self.city}"
    
    class Meta:
        db_table = 'addresses'  # Name of the existing table
        managed = False  # Don't let Django manage this table (no migrations)
        

class Customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    address = models.ForeignKey('Address', on_delete=models.SET_NULL, null=True)  # one-to-many
    phone_no = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    password = models.CharField(max_length=30)
    wishlist = ArrayField(models.IntegerField())

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'customer'  # Name of the existing table
        managed = False  # Don't let Django manage this table (no migrations)