from django.db import models

# Create your models here.
class Customer(models.Model):
    name=models.CharField( max_length=150)
    phone=models.CharField( max_length=50,unique=True)
    email=models.EmailField( max_length=254)
    address=models.CharField( max_length=250,blank=True,null=True)
    def __str__(self):
        return self.name+(self.phone[-1:-4])