from django.contrib import admin
from .models import *
 # Register your models here.
class pos_adm(admin.ModelAdmin):
    list_display=['customer_id','order_no','date_entry']
admin.site.register(POS,pos_adm)

class order_adm(admin.ModelAdmin):
    list_display=['medicine_name','customer','order_number',
'quantity',
'unit',
'batch_id','price_per','total_price']
admin.site.register(Order,order_adm)

class Invoice_adm(admin.ModelAdmin):
    list_display=['uni_id','pos_order','date_entry','Total_Price','med_name','order_items','order_unit','items_price','items_expiry','payment_method']
admin.site.register(Invoice,Invoice_adm)

class Return_adm(admin.ModelAdmin):
    list_display=[
    'invoice_no','date'
        
    ]
admin.site.register(Return,Return_adm)
@admin.register(ReturnDetails)
class Return_detailsadm(admin.ModelAdmin):
    list_display=[
        'inv_number','order_items','returned_item','quantity','unit','batch_id','date','order_items_price','total_price_order'
    ]

@admin.register(ReturnPurchase)
class ReturnPurchaseAdm(admin.ModelAdmin):
    list_display=[
        'medicine_name',
'supplier_name',
'quantity',
'unit',
'last_purchase_id',
'batch_id',
'date'
    ]