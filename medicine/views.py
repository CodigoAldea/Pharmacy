from django.shortcuts import render,redirect
from .models import *
from supplier.models import Supplier
from stocks.models import *
from manufacturer.models import *
from django.db.models import F, Value
# Create your views here.
def medicine_home(request):
    medicine=Medicine.objects.all().order_by('-id')
    manufac_det=Manufacturer.objects.all()
    med_tye_det=Medicine_type.objects.all()
    if request.method=='POST':
        name=request.POST.get("name")
        strength=request.POST.get("strength")
        generic=request.POST.get("generic")
        med_type=request.POST.get("type")
        manufac=request.POST.get("manufacturer")
        if name:
            med_type_obj=Medicine_type.objects.get(type_name=med_type)
            if Manufacturer.objects.filter(manufac_name=manufac):
                manufac_obj=Manufacturer.objects.get(manufac_name=manufac)
            else:
                manufac_crt=Manufacturer.objects.create(manufac_name=manufac)
                manufac_crt.save()
                manufac_obj=Manufacturer.objects.get(manufac_name=manufac)
            m=Medicine.objects.create(name=name,strength=strength,generic_name=generic,med_type=med_type_obj,manufacturer=manufac_obj)
            m.save()
            return redirect('medicine_home')
    context={'medicine':medicine,'manufac_det':manufac_det,'medicine_type':med_tye_det}
    return render(request,'medicine/medicine.html',context)