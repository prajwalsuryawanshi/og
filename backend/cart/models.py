from django.db import models
from customer.models import Customer
from products.models import Product

class Cart(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to Customer model
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)    # Link to Product model
    total = models.DecimalField(max_digits=10, decimal_places=2)  
    qty = models.PositiveIntegerField()  

    def __str__(self):
        return f"Cart {self.id} for Customer {self.customer.name}"
