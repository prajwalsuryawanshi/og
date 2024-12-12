from django.db import models
from django.db.models import UniqueConstraint

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE, db_column='customer_id')  # No need to specify `to_field`
    address_id = models.ForeignKey('customer.Address', on_delete=models.CASCADE, db_column='address_id') # Optional, nullable address
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'  # Keep this if the table name in the database is specifically 'orders'
        # Remove managed=False unless you don't want Django to manage the table

    def __str__(self):
        return str(self.order_id)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE, db_column='product_id') # Optional, nullable address
    quantity = models.PositiveIntegerField()

    class Meta:
        db_table = 'order_items'
        constraints = [
            UniqueConstraint(fields=['order', 'product'], name='unique_order_product')
        ]  # Prevent duplicate products in the same order

    def __str__(self):
        return f"Order {self.order.order_id} - Product {self.product.product_id}"  # Using product_id from Product model