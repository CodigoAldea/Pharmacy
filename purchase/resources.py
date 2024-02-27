# resources.py
from import_export import resources
from .models import YourModel, Purchase_details

class YourModelResource(resources.ModelResource):
    class Meta:
        model = YourModel
class PurchaseResource(resources.ModelResource):
    class Meta:
        model = Purchase_details