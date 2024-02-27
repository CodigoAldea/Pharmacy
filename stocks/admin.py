from django.contrib import admin
from .models import *
# Register your models here.
class batch_adm(admin.ModelAdmin):
    list_display=[    'batch_id','expiry','entry']
admin.site.register(batch,batch_adm)

class Stocks_adm(admin.ModelAdmin):
    list_display=['last_purchase','medicine_name','batch_id','quantity','strips_per_box','strips','tabs_per_strip','pieces','expiry_date','entry_date']
admin.site.register(Stocks,Stocks_adm)

