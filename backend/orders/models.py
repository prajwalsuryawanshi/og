from django.db import models

class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer_id = models.ForeignKey('customer.Customer', on_delete=models.CASCADE,db_column='customer_id', to_field='customer_id')
    product_id = models.ForeignKey('products.Product', on_delete=models.CASCADE,db_column='product_id', to_field='product_id')
    quantity = models.IntegerField()
    address = models.CharField(max_length=511)
    order_total = models.DecimalField(max_digits=10, decimal_places=2)
    order_status = models.CharField(max_length=255)
    payment_type = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        managed = False

    def __str__(self):
        return str(self.order_id)
