from django.db import models

# Create your models here.
class Manufacturer(models.Model):
    manufac_name=models.CharField( max_length=250,unique=True)
    def __str__(self):
        return self.manufac_name 