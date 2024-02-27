from django.shortcuts import render, redirect
from .models import *
from supplier.models import Supplier
from stocks.models import *
from medicine.models import *
from django.db.models import F, Value
from tablib import Dataset
from .resources import *
from django.contrib import messages
import csv, io

# Purchase Home View
def purchase_home(request):
    # Retrieve data for rendering the purchase home page
    purchase=Purchase_details.objects.all().order_by('-id')[:4]
    stock = Stocks.objects.all()
    medicine = Medicine.objects.all()
    batches = batch.objects.all()
    suppliers = Supplier.objects.all()

    if request.method == 'GET':
        # Get parameters from the query string for filtering
        supplier = request.GET.get("supplier")
        medicine_name = request.GET.get("name")
        quantity = request.GET.get("quantity")
        batch_id = request.GET.get("batch_id")
        expiry = request.GET.get("expiry")
        box_size = request.GET.get("box_size")
        box_cost = request.GET.get("box_cost")
        box_sell = request.GET.get("box_sell")
        tabs_strip = request.GET.get("tabs_strip")
        strip_cost = request.GET.get("strip_cost")
        strip_sell = request.GET.get("strip_sell")
        tabs_cost = request.GET.get("tabs_cost")
        tabs_sell = request.GET.get("tabs_sell")
        type_med=request.GET.get("type")
        manufac=request.GET.get("manufacturer")
        strength=request.GET.get("strength")
        generic=request.GET.get("generic")
        supp_phone=request.GET.get("phone")
        supp_email=request.GET.get("email")
        supp_add=request.GET.get("address")
        
        if supplier:
            if Medicine_type.objects.filter(type_name=type_med):
                pass
            else:
                type_crt=Medicine_type.objects.create(type_name=type_med)
                type_crt.save()
            if Manufacturer.objects.filter(manufac_name=manufac):
                pass
            else:
                manuf_crt=Manufacturer.objects.create(manufac_name=manufac)
                manuf_crt.save()
            if Medicine.objects.filter(name=medicine_name):
                pass
            else:
                med_crt=Medicine.objects.create(name=medicine_name,strength=strength,generic_name=generic,med_type=Medicine_type.objects.get(type_name=type_med),manufacturer=Manufacturer.objects.get(name=manufac))
                med_crt.save()
            if Supplier.objects.filter(name=supplier):
                pass
            else:
                supp_crt=Supplier.objects.create(name=supplier,phone=supp_phone,email=supp_email,adddress=supp_add)
                supp_crt.save()
            # Create a new purchase record
            supplier_id = Supplier.objects.get(name=supplier)
            medicine_id = Medicine.objects.get(name=medicine_name)
            last_purchase = Purchase_details.objects.last()
            un_id = 0

            if last_purchase:
                un_id += (int(last_purchase.unique_id) + 1)
            else:
                un_id += 1

            x = Purchase_details.objects.create(
                unique_id=un_id, supplier=supplier_id, medicine_name=medicine_id, quantity=quantity, batch_id=batch_id,
                expiry=expiry, box_size=box_size, box_cp=box_cost, box_sp=box_sell, tabs_strip=tabs_strip,
                strip_cp=strip_cost, strip_sp=strip_sell, tabs_cp=tabs_cost, tabs_sp=tabs_sell
            )
            x.save()

            batch_upd = batch.objects.filter(batch_id=batch_id)

            if batch_upd:
                pass
            else:
                # Create a new batch if it doesn't exist
                b = batch.objects.create(batch_id=batch_id, expiry=expiry)
                b.save()

            purchase_id = Purchase_details.objects.get(unique_id=un_id)
            batch_inp = batch.objects.get(batch_id=batch_id)
            stock_check = Stocks.objects.filter(medicine_name=medicine_id, batch_id=batch_inp)

            if stock_check:
                # Update stock if it exists
                Stocks.objects.filter(medicine_name=medicine_id, batch_id=batch_inp).update(
                    quantity=F('quantity') + Value(purchase_id.quantity),
                    strips=F('strips') + Value(purchase_id.quantity * purchase_id.box_size),
                    pieces=F('pieces') + Value(purchase_id.quantity * purchase_id.box_size * purchase_id.tabs_strip),
                    entry_date=purchase_id.entry, last_purchase=purchase_id
                )
            else:
                # Create a new stock entry if it doesn't exist
                s = Stocks.objects.create(
                    last_purchase=purchase_id, medicine_name=medicine_id, batch_id=batch_inp, quantity=purchase_id.quantity,
                    entry_date=purchase_id.entry, strips=purchase_id.quantity * (purchase_id.box_size),
                    pieces=purchase_id.quantity * (purchase_id.box_size) * (purchase_id.tabs_strip)
                )
                s.save()

            return redirect('purchase_home')

    context = {'stock': stock, 'medicine': medicine, 'batches': batches, 'suppliers': suppliers, 'purchase': purchase}
    return render(request, 'purchase/purchase.html', context)

def purchase_history(request):
    purchase=Purchase_details.objects.all().order_by('-id')
    return render(request,'purchase/purchase_history.html',{'purchase':purchase})

# Import File View
def import_file(request):
    if request.method == 'POST':
        # Handle CSV file import
        my_resource = PurchaseResource()
        dataset = Dataset()
        new = request.FILES['my_file']

        # Check if the file is a CSV
        if not new.name.endswith('csv'):
            messages.info(request, 'Please upload a valid CSV file.')
            return render(request, 'purchase/import.html')
        else:
            messages.info(request, 'File uploaded successfully.')

        data_set = new.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)

        # Iterate through CSV columns and create YourModel records
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            if Medicine_type.objects.filter(type_name=column[14]):
                pass
            else:
                type_crt=Medicine_type.objects.create(type_name=column[14])
                type_crt.save()
            if Manufacturer.objects.filter(manufac_name=column[15]):
                pass
            else:
                manuf_crt=Manufacturer.objects.create(manufac_name=column[15])
                manuf_crt.save()
            if Medicine.objects.filter(name=column[2]):
                pass
            else:
                med_crt=Medicine.objects.create(name=column[2],strength=column[16],generic_name=column[17],med_type=Medicine_type.objects.get(type_name=column[14]),manufacturer=Manufacturer.objects.get(manufac_name=column[15]))
                med_crt.save()
            if Supplier.objects.filter(name=column[1]):
                pass
            else:
                supp_crt=Supplier.objects.create(name=column[1],phone=column[18],email=column[19],adddress=column[20])
                supp_crt.save()
                
            purchase, created = Purchase_details.objects.update_or_create(
                unique_id=(int(Purchase_details.objects.last().id) + 1), supplier=(Supplier.objects.get(name=column[1])), medicine_name=(Medicine.objects.get(name=column[2])), quantity=column[3],
                batch_id=column[4], expiry=column[5], box_size=column[6], box_cp=column[7], box_sp=column[8],
                tabs_strip=column[9], strip_cp=column[10], strip_sp=column[11], tabs_cp=column[12], tabs_sp=column[13]
                
            )
            batch_upd, created=batch.objects.update_or_create(batch_id=column[4], defaults={'expiry':column[5], 'entry':purchase.entry})
            old_quantity=Stocks.objects.filter(medicine_name=Medicine.objects.get(name=column[2]), batch_id=batch.objects.get(batch_id=column[4]))
            if old_quantity:
                stock_upd, created=Stocks.objects.update_or_create(medicine_name=Medicine.objects.get(name=column[2]),
                                                           batch_id=batch.objects.get(batch_id=column[4]), defaults={'quantity':F('quantity')+int(column[3]), 'strips':F('strips')+int(column[6])*int(column[3]), 'pieces':F('pieces')+int(column[6])*int(column[3])*int(column[9]),  'last_purchase':purchase, 'entry_date':purchase.entry})
            else:
                stock_upd, created=Stocks.objects.update_or_create(medicine_name=Medicine.objects.get(name=column[2]),
                                                                   batch_id=batch.objects.get(batch_id=column[4]), defaults={'quantity':int(column[3]), 'strips':int(column[6])*int(column[3]), 'pieces':int(column[6])*int(column[3])*int(column[9]),  'last_purchase':purchase, 'entry_date':purchase.entry})
        return redirect('purchase_home')

    return render(request, 'purchase/import.html')
