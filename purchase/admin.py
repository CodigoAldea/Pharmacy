from django.contrib import admin
from .models import *
# Register your models here.
class Purchase_adm(admin.ModelAdmin):
    list_display=['unique_id','supplier','medicine_name','quantity','batch_id','expiry','entry','box_size','box_cp','box_sp','tabs_strip','strip_cp','strip_sp','tabs_cp','tabs_sp']
admin.site.register(Purchase_details,Purchase_adm)

@admin.register(YourModel)
class YourModelAdm(admin.ModelAdmin):
    list_display=['name','description']