from django.db import models
from medicine.models import Medicine
from supplier.models import Supplier
import uuid

class Purchase_details(models.Model):
    # Purchase_details model representing details of medicine purchases
    unique_id = models.IntegerField(null=True, blank=True, unique=True, help_text="Unique identifier for the purchase details")
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, help_text="Supplier of the medicine")
    medicine_name = models.ForeignKey(Medicine, on_delete=models.CASCADE, help_text="Medicine being purchased")
    quantity = models.IntegerField(help_text="Quantity of medicine purchased")
    batch_id = models.CharField(max_length=100, help_text="Batch ID of the purchased medicine")
    expiry = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, help_text="Expiry date of the medicine")
    entry = models.DateField(auto_now=False, auto_now_add=True, help_text="Date of purchase entry")
    box_size = models.IntegerField(help_text="Number of strips per box")
    box_cp = models.FloatField(("Box Cost"), help_text="Cost price of the entire box")
    box_sp = models.FloatField(("Box Sell"), help_text="Selling price of the entire box")
    tabs_strip = models.IntegerField(help_text="Number of tablets per strip")
    strip_cp = models.FloatField(("Strip Cost"), help_text="Cost price of a strip")
    strip_sp = models.FloatField(("Strip Sell"), help_text="Selling price of a strip")
    tabs_cp = models.FloatField(("Piece Cost"), help_text="Cost price of a tablet")
    tabs_sp = models.FloatField(("Piece Sell"), help_text="Selling price of a tablet")

    def __str__(self):
        return str(self.unique_id)

class YourModel(models.Model):
    # YourModel model with basic fields
    name = models.CharField(max_length=100, help_text="Name of the model")
    description = models.TextField(help_text="Description of the model")

    def __str__(self):
        return self.name
