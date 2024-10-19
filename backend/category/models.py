from django.db import models

# Create your models here.
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=255)

    class Meta:
        db_table = 'category'  # Name of the existing table
        managed = False  # Don't let Django manage this table (no migrations)

    def __str__(self):
        return self.category_name