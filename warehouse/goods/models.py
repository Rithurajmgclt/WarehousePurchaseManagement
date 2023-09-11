from django.db import models

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_stock = models.PositiveIntegerField(default=25000)

    def __str__(self):
        return self.name

class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    purchase_id = models.CharField(max_length=255, unique=True)
    purchased_qty = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)