from django.http import JsonResponse
from django.shortcuts import render,redirect
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from django.views import View
from medicine.models import *
from accounts.models import *
from stocks.models import *
from .models import *
from django.utils import timezone
from .forms import *
from xhtml2pdf import pisa
from django.contrib import messages 
from django.core.serializers import serialize
# from reportlab.pdfgen import canvas
# Create your views here.

# View for the Point of Sale (POS) home page
def fetch_data_from_database(request):
    phone_number = request.GET.get("phone", "")
    try:
        customer = Customer.objects.get(phone=phone_number)
        data = {
            "name": customer.name,
            "email": customer.email,
            "address": customer.address,
            # Add more fields as needed
        }
        return JsonResponse(data)
    except Customer.DoesNotExist:
        data = {
            "name": '',
            "email": '',
            "address": '',
            # Add more fields as needed
        }
        return JsonResponse(data)
def fetch_batch_ids(request):
    medicine_name = request.GET.get("medicine", "")
    batch_ids = Stocks.objects.filter(medicine_name__name=medicine_name).values_list('batch_id__batch_id', flat=True)
    print(batch_ids)
    return JsonResponse(list(batch_ids), safe=False)
def pos_home(request):
    # Check if there is an active invoice session
    inv_ses = request.session.get('pos_inv_id')
    phone_info=request.session.get('phone')
    
    if inv_ses:
        if request.method=='GET':
            new=request.GET.get('new')
            if new:
                if phone_info:
                    del request.session['phone']
                del request.session['pos_inv_id']
                return redirect('pos_home')
    # Retrieve necessary data for the POS page
    medicine_bar = Stocks.objects.all()
    customer_bar=Customer.objects.all()
    batch_id_bar=batch.objects.all()
    if POS.objects.filter(order_no=inv_ses):
        inv_obj=Invoice.objects.filter(pos_order=POS.objects.get(order_no=inv_ses))
    else:
        inv_obj=None
    if inv_obj is not None:
        order_obj=Order.objects.filter(customer_id=inv_obj[0].pos_order)
    else:
        order_obj=None
    print(inv_obj)
    context={
        'medicine':medicine_bar,
        'customer':customer_bar,
        'batch':batch_id_bar,
        'inv_id':inv_ses,
        'cust_info':inv_obj,
        'order_info':order_obj,
        'phone_info':phone_info
             }
    if request.method == 'POST':
            # Handle the POS form submission
        phone=request.POST.get('phone')
        name=request.POST.get('name')
        medicine=request.POST.get('medicine').upper()
        batch_id=request.POST.get('batch_id')
        quantity=request.POST.get('quantity')
        unit=request.POST.get('unit')
        email=request.POST.get('email')
        address=request.POST.get('address')
        #check for medicne name
        if phone:
            request.session['phone']=phone
            cust_obj_srch=Customer.objects.filter(phone=phone)
            if cust_obj_srch:
                cust_obj=Customer.objects.get(phone=phone)
            else:
                if email:
                    if address:
                        cust_obj_crt=Customer.objects.create(phone=phone,name=name,email=email,address=address)
                        cust_obj_crt.save()
                    else:
                        cust_obj_crt=Customer.objects.create(phone=phone,name=name,email=email)
                        cust_obj_crt.save()
                else:
                    cust_obj_crt=Customer.objects.create(phone=phone,name=name)
                    cust_obj_crt.save()
        if not Medicine.objects.filter(name=medicine):
            messages.error(request,'Medicine not found')
            return redirect('pos_home')
        elif not batch.objects.filter(batch_id=batch_id):
            messages.error(request,'Batch-ID not found')
            return redirect('pos_home')
        else:
            if not Stocks.objects.filter(medicine_name=Medicine.objects.get(name=medicine)):
                messages.error(request,'Medicine not in Stock')
                return redirect('pos_home')
            else:
                if not Stocks.objects.filter(medicine_name=Medicine.objects.get(name=medicine),batch_id=batch.objects.get(batch_id=batch_id)):
                    messages.error(request,'Batch-ID is out of stock')
                    return redirect('pos_home')
                else:
        # Code to process the POS form data
                        if phone:
                            cust_obj=Customer.objects.get(phone=phone)
                            medicine_obj=Medicine.objects.get(name=medicine)
                            batch_obj=batch.objects.get(batch_id=batch_id)
                            pos_check=POS.objects.filter(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date())
                            if pos_check:
                                pos_id=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date())
                            else:
                                order_number_last=POS.objects.last()
                                if order_number_last:
                                    pos=POS.objects.create(customer_id=cust_obj,order_no=(order_number_last.order_no+1))
                                    pos.save()
                                    print(timezone.localtime(timezone.now()).date())
                                    pos_id=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date())
                                else:
                                    pos=POS.objects.create(customer_id=cust_obj,order_no=(1))
                                    pos.save()
                                    pos_id=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date())
                            
                            
                            order_check=Order.objects.filter(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj)
                            if order_check:
                                order_upd=Order.objects.get(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj)
                                Order.objects.filter(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj).update(quantity=(order_upd.quantity+int(quantity)))
                            else:
                                order_crt=Order.objects.create(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj,quantity=quantity,unit=unit)
                                order_crt.save()
                            stock_upd=Stocks.objects.get(medicine_name=medicine_obj,batch_id=batch_obj)
                            if unit=='piece':
                                stock_upd.pieces -= int(quantity)
                                stock_upd.save()
                            elif unit=='strip':
                                stock_upd.strips -= int(quantity)
                                stock_upd.save()
                            elif unit=='box':
                                stock_upd.quantity -= int(quantity)
                                stock_upd.save()
                            stock_upd.update_quantity()
                            invoice_check=Invoice.objects.filter(pos_order=pos_id)
                            if invoice_check:
                                invoice_get=Invoice.objects.get(pos_order=pos_id)
                                request.session['pos_inv_id']=invoice_get.pos_order.order_no
                            else:
                                invoice_crt=Invoice.objects.create(pos_order=pos_id)
                                invoice_crt.save()
                                invoice_get=Invoice.objects.get(pos_order=pos_id)
                                request.session['pos_inv_id']=invoice_get.pos_order.order_no
                            return redirect('pos_home')
                    
                        elif medicine and inv_ses:
                            if POS.objects.filter(order_no=inv_ses):
                                if Invoice.objects.filter(pos_order=POS.objects.get(order_no=inv_ses)):
                                    cust_obj=Customer.objects.get(phone=Invoice.objects.get(pos_order=POS.objects.get(order_no=inv_ses)).pos_order.customer_id.phone)
                                    print(cust_obj)
                            else:
                                print(phone_info)
                                cust_obj=Customer.objects.get(phone=phone_info)
                            medicine_obj=Medicine.objects.get(name=medicine)
                            batch_obj=batch.objects.get(batch_id=batch_id)
                            pos_check=POS.objects.filter(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date())
                            if pos_check:
                                pass
                            else:
                                order_number_last=POS.objects.last()
                                if order_number_last:
                                    pos=POS.objects.create(customer_id=cust_obj,order_no=(order_number_last.order_no+1))
                                    pos.save()
                                else:
                                    pos=POS.objects.create(customer_id=cust_obj,order_no=(1))
                                    pos.save()
                                inv_check=Invoice.objects.filter(pos_order=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date()))
                                if inv_check:
                                    invoice_get=Invoice.objects.get(pos_order=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date()))
                                    request.session['pos_inv_id']=invoice_get.pos_order.order_no
                                else:
                                    invoice_crt=Invoice.objects.create(pos_order=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date()))
                                    invoice_crt.save()
                                    invoice_get=Invoice.objects.get(pos_order=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date()))
                                    request.session['pos_inv_id']=invoice_get.pos_order.order_no
                            pos_id=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date())
                            order_check=Order.objects.filter(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj)
                            if order_check:
                                order_upd=Order.objects.get(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj)
                                Order.objects.filter(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj).update(quantity=(order_upd.quantity+int(quantity)))
                            else:
                                order_crt=Order.objects.create(medicine_name=medicine_obj,customer=pos_id,batch_id=batch_obj,quantity=quantity,unit=unit)
                                order_crt.save()
                            stock_upd=Stocks.objects.get(medicine_name=medicine_obj,batch_id=batch_obj)
                            if unit=='piece':
                                stock_upd.pieces -= int(quantity)
                                stock_upd.save()
                            elif unit=='strip':
                                stock_upd.strips -= int(quantity)
                                stock_upd.save()
                            elif unit=='box':
                                stock_upd.quantity -= int(quantity)
                                stock_upd.save()
                            stock_upd.update_quantity()
                            invoice_check=Invoice.objects.filter(pos_order=pos_id)
                            invoice_get=Invoice.objects.get(pos_order=POS.objects.get(customer_id=cust_obj,date_entry=timezone.localtime(timezone.now()).date()))
                            request.session['pos_inv_id']=invoice_get.pos_order.order_no
                            return redirect('pos_home')
                    
    return render(request,'pos/pos.html',context)

def delete_order(request,ord_id):
    order_del=Order.objects.get(id=ord_id)
    pos_del=POS.objects.get(id=order_del.customer.id)
    stock_upd_med=order_del.medicine_name.id
    stock_upd_qty=order_del.quantity
    stock_upd_unit=order_del.unit
    stock_upd_batch=order_del.batch_id
    stock_upd_get=Stocks.objects.get(medicine_name=stock_upd_med,batch_id=stock_upd_batch)
    if stock_upd_unit=='piece':
        stock_upd_get.pieces += int(stock_upd_qty)
        stock_upd_get.save()
    elif stock_upd_unit=='strip':
        stock_upd_get.strips += int(stock_upd_qty)
        stock_upd_get.save()
    elif stock_upd_unit=='box':
        stock_upd_get.quantity += int(stock_upd_qty)
        stock_upd_get.save()
    print(stock_upd_med,stock_upd_qty,stock_upd_unit,stock_upd_batch)
    order_del.delete()
    if Order.objects.filter(customer=pos_del):
        print('ritik')
    else:
        pos_del.delete()
    return redirect('pos_home')
def delete_invoice(request,inv_id):
    inv_del=Invoice.objects.get(id=inv_id)
    inv_del.delete()
    return redirect('pos_home')
# View for processing returns
def return_home(request):
    inv_ses=request.session.get('inv_id')
    medicine_bar = Medicine.objects.all()
    invoice_hist=Invoice.objects.all().order_by('-id')
    if inv_ses:
        if request.method=='GET':
            new=request.GET.get('new')
            if new:
                # Clear the invoice session
                del request.session['inv_id']
                return redirect('return_home')
        
        if request.method == 'POST':
            # Handle the return form submission
            med = request.POST.get('medicine')
            batch_id=request.POST.get('batch_id')
            qnty=request.POST.get('return')
            unit=request.POST.get('unit')
            # Code to process return form data
            med_obj=Medicine.objects.get(name=med)
            batch_obj=batch.objects.get(batch_id=batch_id)
            inv_obj=Invoice.objects.get(id=inv_ses)
            if Return.objects.filter(invoice_no=inv_obj):
                pass
            else:
                return_create=Return.objects.create(invoice_no=inv_obj)
                return_create.save()
            return_data=ReturnDetails.objects.create(inv_number=(Return.objects.get(invoice_no=inv_obj)),returned_item=med_obj,quantity=qnty,batch_id=batch_obj,unit=unit)
            return_data.save()
            if Stocks.objects.filter(medicine_name=med_obj,batch_id=batch_obj):
                stock_upd=Stocks.objects.get(medicine_name=med_obj,batch_id=batch_obj)
                if unit=='piece':
                    stock_upd.pieces += int(qnty)
                    stock_upd.save()
                elif unit=='strip':
                    stock_upd.strips += int(qnty)
                    stock_upd.save()
                elif unit=='box':
                    stock_upd.quantity += int(qnty)
                    stock_upd.save()
                stock_upd.update_quantity()
                return redirect('return_home')
            else:
                if unit=='piece':
                    x=Stocks.objects.create(medicine_name=med_obj,batch_id=batch_obj,pieces=int(qnty),last_purchase=Purchase_details.objects.get(medicine_name=med_obj,batch_id=batch_obj)) 
                    x.save()
                elif unit=='strip':
                    x=Stocks.objects.create(medicine_name=med_obj,batch_id=batch_obj,strips=int(qnty),last_purchase=Purchase_details.objects.get(medicine_name=med_obj,batch_id=batch_obj))
                    x.save()
                elif unit=='box':
                    x=Stocks.objects.create(medicine_name=med_obj,batch_id=batch_obj,quantity=int(qnty),last_purchase=Purchase_details.objects.get(medicine_name=med_obj,batch_id=batch_obj))
                    x.save()
                return redirect('return_home')
        else:
            # Display the return form
            cust_inv=Invoice.objects.get(id=inv_ses)
            final_invoices=Order.objects.filter(customer=cust_inv.pos_order)
            return_invoices=None
            invoice_total_return=0
            if inv_ses:
                if Invoice.objects.filter(id=inv_ses):
                    if Return.objects.filter(invoice_no=(Invoice.objects.get(id=inv_ses))):
                        return_invoices=ReturnDetails.objects.filter(inv_number=(Return.objects.get(invoice_no=(Invoice.objects.get(id=inv_ses)))))
                        invoice_total_return=sum(float(i.total_price_order) for i in return_invoices)
                        
            return render(request,'pos/return.html',{'cust_inv':cust_inv,'inv_id':inv_ses,'invoices':final_invoices,'return_invoices':return_invoices,'medicines':medicine_bar,'invoice_total_return':invoice_total_return})
    else:
        if request.method=="POST":
            form=ReturnForm(request.POST)
            if form.is_valid():
                request.session['inv_id']=str((form.cleaned_data['invoice_no']).id)
                return redirect('return_home')
        else:
            form=ReturnForm()
        return render(request,'pos/return.html',{'form':form,'inv_id':inv_ses,'medicines':medicine_bar,'history_inv':invoice_hist})
def return_details(request):
    return_hist=ReturnDetails.objects.all().order_by('-id')
    context={
        'return_hist':return_hist
    }
    return render(request,'pos/return_details.html',context)
# Function to render HTML to PDF
def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
    
	return None
# View for testing purposes
def test(request):
    inv_ses=request.session.get('inv_id')
    inv_det=Invoice.objects.filter(id=inv_ses)
    return render(request,'test.html')


#Opens up page as PDF
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        inv=request.session.get('inv_id')
        if inv:
            cust_inv = Invoice.objects.get(id=inv)
        else:
            inv = request.session.get('pos_inv_id')
            cust_inv = Invoice.objects.get(id=inv)
        cust_inv=Invoice.objects.get(id=inv)
        final_invoices=Order.objects.filter(customer=cust_inv.pos_order)
        return_invoices=None
        invoice_total_return=0
        updated_balance=0
        if inv:
            if Invoice.objects.filter(id=inv):
                if Return.objects.filter(invoice_no=(Invoice.objects.get(id=inv))):
                    return_invoices=ReturnDetails.objects.filter(inv_number=(Return.objects.get(invoice_no=(Invoice.objects.get(id=inv)))))
                    invoice_total_return=sum(float(i.total_price_order) for i in return_invoices)
                    updated_balance=float(cust_inv.Total_Price())-float(invoice_total_return)
        data={'invoices':final_invoices,"company": "Ritik Pharmacy Company",
	    "address": "123 Street name",
	    "city": "Durg",
	    "state": "C.G.",
	    "zipcode": "491001",
	    "phone": "1234567890",
	    "email": "pharma@bsuiness.com",
	    "website": "pharmacy.com",'total':cust_inv,'cust_id':inv
        ,'return_invoices':return_invoices,
        'invoice_total_return':invoice_total_return,
        'updated_balance':updated_balance
        }
        
        pdf = render_to_pdf('pdf_template.html', data)
        return HttpResponse(pdf, content_type='application/pdf')


# Automatically downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        inv = request.session.get('inv_id')
        if inv:
            cust_inv = Invoice.objects.get(id=inv)
        else:
            inv = request.session.get('pos_inv_id')
            cust_inv = Invoice.objects.get(id=inv)
        final_invoices = Order.objects.filter(customer=cust_inv.pos_order)
        return_invoices=None
        invoice_total_return=0
        updated_balance=0
        if inv:
            if Invoice.objects.filter(id=inv):
                if Return.objects.filter(invoice_no=(Invoice.objects.get(id=inv))):
                    return_invoices=ReturnDetails.objects.filter(inv_number=(Return.objects.get(invoice_no=(Invoice.objects.get(id=inv)))))
                    invoice_total_return=sum(float(i.total_price_order) for i in return_invoices)
                    updated_balance=float(cust_inv.Total_Price())-float(invoice_total_return)
        data = {
            'invoices': final_invoices,
            "company": "Ritik Pharmacy Company",
            "address": "123 Street name",
            "city": "Durg",
            "state": "C.G.",
            "zipcode": "491001",
            "phone": "1234567890",
            "email": "pharma@bsuiness.com",
            "website": "pharmacy.com",
            'total': cust_inv,
            'cust_id': inv
            ,'return_invoices':return_invoices,
        'invoice_total_return':invoice_total_return,
        'updated_balance':updated_balance
        }
        pdf = render_to_pdf('pdf_template.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response
    

    
def return_purchase(request):
    med=Stocks.objects.all()
    return_hist=ReturnPurchase.objects.all().order_by('-id')
    if request.method=="POST":
            form=ReturnPurchaseForm(request.POST)
            if form.is_valid():
                request.session['stock_id']=(form.cleaned_data['medicine_name']).upper()
                request.session['batch_id']=(form.cleaned_data['batch_id'])
                return redirect('return_purchase')
            else:
                return redirect('return_purchase')
    stock_id=request.session.get('stock_id')
    batch_id=request.session.get('batch_id')
    if stock_id:
        form=ReturnPurchaseForm()
        del request.session['stock_id']
        med_name=Medicine.objects.filter(name=stock_id)
        if batch_id:
            del request.session['batch_id']
            batch_id_obj=batch.objects.filter(batch_id=batch_id)
            if batch_id_obj:
                        stock_sts=Stocks.objects.filter(medicine_name=Medicine.objects.get(name=stock_id),batch_id=batch.objects.get(batch_id=batch_id))
                        return render(request,'pos/return_purchase.html',{'form':form,'stock_sts':stock_sts,'medicines':med})
        if med_name:
                    stock_sts=Stocks.objects.filter(medicine_name=Medicine.objects.get(name=stock_id))
                    return render(request,'pos/return_purchase.html',{'form':form,'stock_sts':stock_sts,'medicines':med})
        return redirect('return_purchase')
    else:
        form=ReturnPurchaseForm()
    context={
        'form':form,
        'medicines':med,
        'return_hist':return_hist
        }
    return render(request,'pos/return_purchase.html',context)    
def delete_stock(request,stock_id):
    stock_del=Stocks.objects.get(id=stock_id)
    if stock_del.quantity==0:
        if stock_del.strips>0:
            purc_ret=ReturnPurchase.objects.create(medicine_name=stock_del.medicine_name.name,batch_id=stock_del.batch_id,quantity=stock_del.strips,unit='strips',supplier_name=stock_del.last_purchase.supplier.name,last_purchase_id=stock_del.last_purchase.id)
            purc_ret.save()
        else:
            pass
    else:
        purc_ret=ReturnPurchase.objects.create(medicine_name=stock_del.medicine_name.name,batch_id=stock_del.batch_id,quantity=stock_del.quantity,unit='box',supplier_name=stock_del.last_purchase.supplier.name,last_purchase_id=stock_del.last_purchase.id)
        purc_ret.save()
    stock_del.delete()
    return redirect('return_purchase')

def invocie_relocate(request,inv_id):
    request.session['inv_id']=inv_id
    return redirect('return_home')
def update_order(request):
    if request.method == 'POST'and request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        print('ritik')
        # Get data from POST request
        medicine_name = request.POST.get('medicine_name')
        batch_id = request.POST.get('batch_id')
        quantity =int( request.POST.get('quantity'))
        unit = request.POST.get('unit')
        phone=request.POST.get('phone_info')
        print(medicine_name,batch_id,quantity,unit,phone)
        order = Order.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id), customer=POS.objects.get(order_no=request.session.get('pos_inv_id')))
        old_quantity=order.quantity
        old_unit=order.unit
        if old_quantity>quantity and old_unit==unit=='box':
            diff=old_quantity-quantity
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.quantity=stock_upd.quantity+diff
            stock_upd.save()
        elif old_quantity<quantity and old_unit==unit=='box':
            diff=quantity-old_quantity
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.quantity=stock_upd.quantity-diff
            stock_upd.save()
        elif old_quantity>quantity and old_unit==unit=='strip':
            diff=old_quantity-quantity
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.strips=stock_upd.strips+diff
            stock_upd.save()
        elif old_quantity<quantity and old_unit==unit=='strip':
            diff=quantity-old_quantity
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.strips=stock_upd.strips-diff
            stock_upd.save()
        elif old_quantity>quantity and old_unit==unit=='piece':
            diff=old_quantity-quantity
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.pieces=stock_upd.pieces+diff
            stock_upd.save()
        elif old_quantity<quantity and old_unit==unit=='piece':
            diff=quantity-old_quantity
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.pieces=stock_upd.pieces-diff
            stock_upd.save()
        order.quantity = quantity
        if old_unit=='strip'and unit=='box':
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.strips=stock_upd.strips+old_quantity
            stock_upd.quantity=stock_upd.quantity-quantity
            stock_upd.save()
        elif old_unit=='box'and unit=='strip':
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.strips=stock_upd.strips-quantity
            stock_upd.quantity=stock_upd.quantity+old_quantity
            stock_upd.save()
        elif old_unit=='strip'and unit=='piece':
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.pieces=stock_upd.pieces-quantity
            stock_upd.strips=stock_upd.strips+old_quantity
            stock_upd.save()
        elif old_unit=='piece'and unit=='strip':
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.pieces=stock_upd.pieces+old_quantity
            stock_upd.strips=stock_upd.strips-quantity
            stock_upd.save()
        elif old_unit=='box'and unit=='piece':
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.pieces=stock_upd.pieces-quantity
            stock_upd.quantity=stock_upd.quantity+old_quantity
            stock_upd.save()
        elif old_unit=='piece'and unit=='box':
            stock_upd=Stocks.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id))
            stock_upd.pieces=stock_upd.pieces+old_quantity
            stock_upd.quantity=stock_upd.quantity-quantity
            stock_upd.save()
        
        order.unit = unit
        order.save()
        order_new=Order.objects.get(medicine_name=Medicine.objects.get(name=medicine_name), batch_id=batch.objects.get(batch_id=batch_id), customer=POS.objects.get(order_no=request.session.get('pos_inv_id')))
        
        price_per = order_new.price_per()  # Example price per unit
        total_price = order_new.total_price() # Example calculation
        
        # Return updated price and total price along with success message
        return JsonResponse({'message': 'Order updated successfully', 'price_per': price_per, 'total_price': total_price}, status=200)
    else:
        # Return an error response if the request method is not POST
        return JsonResponse({'error': 'Invalid request method'}, status=400)
