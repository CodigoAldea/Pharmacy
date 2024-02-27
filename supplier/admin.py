from django.contrib import admin
from .models import *
# Register your models here.
class Supplier_adm(admin.ModelAdmin):
    list_display=['name','email','adddress','phone']
admin.site.register(Supplier,Supplier_adm)