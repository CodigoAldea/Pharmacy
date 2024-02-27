from django.db import models
from purchase.models import Purchase_details
from medicine.models import Medicine
from django.utils import timezone
from datetime import datetime
# Create your models here.

class batch(models.Model):
    # Batch model representing batches of medicine
    batch_id = models.CharField(max_length=50, unique=True, help_text="Unique identifier for the batch")
    expiry = models.DateField(auto_now=False, auto_now_add=False, help_text="Expiry date of the batch")
    entry = models.DateField(auto_now_add=True, help_text="Date of batch entry")

    def __str__(self):
        return self.batch_id

class Stocks(models.Model):
    # Stocks model representing the current stock of medicine
    last_purchase = models.ForeignKey(Purchase_details, verbose_name=("last_purchase"), on_delete=models.CASCADE, help_text="Last purchase details associated with the stock")
    medicine_name = models.ForeignKey(Medicine, on_delete=models.CASCADE, help_text="Medicine associated with the stock")
    batch_id = models.ForeignKey(batch, verbose_name=("batch"), on_delete=models.CASCADE, null=True, blank=True, help_text="Batch associated with the stock")
    quantity = models.IntegerField(("Box number"), null=True, blank=True, help_text="Number of boxes in stock")
    strips = models.IntegerField(("Strip number"), null=True, blank=True, help_text="Number of strips in stock")
    pieces = models.IntegerField(("Piece number"), null=True, blank=True, help_text="Number of pieces in stock")
    entry_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, help_text="Date of stock entry")

    def expiry_date(self):
        # Get the expiry date from the associated batch, if available
        if self.batch_id:
            return self.batch_id.expiry
        else:
            return None

    def is_expired(self):
        #for testing
        # date_string = '27-12-2024'
        # date_format = '%d-%m-%Y'
        # date_object = datetime.strptime(date_string, date_format).date()
        return self.batch_id.expiry < timezone.now().date()
    def strips_per_box(self):
        return self.last_purchase.box_size
    def tabs_per_strip(self):
        return self.last_purchase.tabs_strip
    def update_quantity(self):
        # Custom logic, if needed
        if (self.pieces/self.strips)<self.last_purchase.tabs_strip:
            self.strips =int(self.pieces/self.last_purchase.tabs_strip) 
            self.save()
        if (self.strips/self.quantity)<self.last_purchase.box_size:
            self.quantity =  int(self.strips/self.last_purchase.box_size) 
            self.save()
    def save(self, *args, **kwargs):
        # Custom logic before saving, if needed
        super(Stocks, self).save(*args, **kwargs)
        # Custom logic after saving, if needed
    def __str__(self):
        return self.medicine_name.name
