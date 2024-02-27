from django.db import models
from manufacturer.models import Manufacturer

# Create your models here.
class Medicine(models.Model):
    name=models.CharField( max_length=250,unique=True)
    strength=models.CharField( max_length=50,null=True,blank=True)
    generic_name=models.CharField( max_length=150)
    med_type=models.ForeignKey("Medicine_type", on_delete=models.CASCADE)
    manufacturer=models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.name}-{self.manufacturer}"
    def save(self, *args, **kwargs):
        # Convert the name field to uppercase before saving
        self.name = self.name.upper()
        super().save(*args, **kwargs)
class Medicine_type(models.Model):
    type_name=models.CharField( max_length=150,unique=True)
    def __str__(self):
        return self.type_name
    