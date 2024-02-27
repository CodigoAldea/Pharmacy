from django.contrib import admin
from .models import *
# Register your models here.
class customer_adm(admin.ModelAdmin):
    list_display=['name',
'phone',
'email',
'address']
admin.site.register(Customer,customer_adm)