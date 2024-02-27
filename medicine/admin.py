from django.contrib import admin
from .models import *
# Register your models here.
class Medicine_adm(admin.ModelAdmin):
    list_display=['name','strength','generic_name','med_type','manufacturer']
admin.site.register(Medicine,Medicine_adm)

class Medicine_type_adm(admin.ModelAdmin):
    list_display=['type_name']
admin.site.register(Medicine_type,Medicine_type_adm)