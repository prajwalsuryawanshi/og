from django.db import models
from django.contrib.postgres.fields import ArrayField

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_description = models.TextField()
    product_images = ArrayField(models.CharField(max_length=255), blank=True, null=True)  # Array for storing multiple image URLs or paths
    category = models.ForeignKey('category.Category', on_delete=models.CASCADE)  # Assuming Category is in 'catalog' app
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'  # Name of the existing table
        managed = False  # Don't let Django manage this table (no migrations)

    def __str__(self):
        return self.product_name
