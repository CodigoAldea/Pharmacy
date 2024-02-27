from django.db import models

# Create your models here.
class Supplier(models.Model):
    name=models.CharField( max_length=200)
    email=models.EmailField( max_length=254)
    adddress=models.TextField()
    phone=models.BigIntegerField()
    def __str__(self):
        return self.name
    