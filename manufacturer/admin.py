from django.contrib import admin
from .models import *
# Register your models here.
class Manuf_adm(admin.ModelAdmin):
    list_display=['manufac_name']
admin.site.register(Manufacturer,Manuf_adm)