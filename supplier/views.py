from django.shortcuts import render,redirect
from .models import *
from .forms import SupplierForm
# Create your views here.

def supplier_home(request):
    supp=Supplier.objects.all()

    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            # Process form data, e.g., save to the database
            return redirect('supplier_home')  # Redirect to a success page
    else:
        form = SupplierForm()

    return render(request,'supplier/supplier.html',{'supplier':supp,'form':form})