from django.shortcuts import render,redirect
from .models import *
from pos.models import *
from .forms import CustPhone,CustName,DateForm
from xhtml2pdf import pisa
from django.views import View
from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template

# Create your views here.

def accounts_home(request):
    date_start_session=request.session.get('date_start')
    date_end_session=request.session.get('date_end')
    if date_start_session:
        del request.session['date_start']
    if date_end_session:
        del request.session['date_end']
    Invoices=Invoice.objects.all().order_by('-id')
    return_hist=ReturnDetails.objects.all().order_by('-id')
    # print(zip(i.order_items(),i.order_unit()))
    if request.method == 'POST':
        # If the form is submitted, process the data
        form = CustPhone(request.POST)
        date_form= DateForm(request.POST)
        if form.is_valid():
            cust_phone = form.cleaned_data['phone']
            cust_obj_fltr=Customer.objects.filter(phone=cust_phone)
            if cust_obj_fltr:
                cust_obj=Customer.objects.get(phone=cust_phone)
                pos_obj=POS.objects.filter(customer_id=cust_obj)
                inv_obj=Invoice.objects.filter(pos_order__in=pos_obj).order_by('-id')
                return_obj=ReturnDetails.objects.filter(inv_number__in=Return.objects.filter(invoice_no__in=inv_obj)).order_by('-id')
                total_spend=0
                total_return=0
                for i in inv_obj:
                    total_spend += float(i.Total_Price())
                for j in return_obj:
                    total_return += float(j.total_price_order)
                difference=total_spend-total_return
                return render(request,'accounts/accounts.html',{'invoices_cust':inv_obj,'cust_obj':cust_obj,'total_spend':difference,'return_hist':return_obj}) 
                
            # return redirect('accounts_home')
            else:
                if date_form.is_valid():
                    date_start = date_form.cleaned_data['date_start']
                    date_end = date_form.cleaned_data['date_end']
                    inv_obj=Invoice.objects.filter(date_entry__range=(date_start, date_end))
                    return_obj=ReturnDetails.objects.filter(date__range=(date_start, date_end))
                    total_spend=0
                    for i in inv_obj:
                        total_spend += float(i.Total_Price())
                    request.session['date_start']=str(date_start)
                    request.session['date_end']=str(date_end)
                    return render(request,'accounts/accounts.html',{'invoices':inv_obj,'date_sort':total_spend,'return_hist':return_obj})
    else:
        # If it's a GET request, render the form
        form = CustPhone()
        date_form= DateForm()
    context={'invoices':Invoices,'form': form,'date_form':date_form,'return_hist':return_hist}
    return render(request,'accounts/accounts.html',context)
def account_cust(request):
    custom=Customer.objects.all()
    if request.method == 'POST':
        # If the form is submitted, process the data
        form = CustName(request.POST)
        if form.is_valid():
            cust_name = form.cleaned_data['name']
            cust_obj_fltr=Customer.objects.filter(name__icontains=cust_name)
            
            return render(request,'accounts/customer.html',{'cust_obj':cust_obj_fltr})
                
        return redirect('accounts_cust')
    else:
        # If it's a GET request, render the form
        form = CustName()
        return render(request,'accounts/customer.html',{'customer':custom,'form':form})

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
    
	return None
class ViewPDF_accounts(View):
    def get(self, request, *args, **kwargs):
        date_start=request.session.get('date_start')
        date_end=request.session.get('date_end')
        inv_obj=Invoice.objects.filter(date_entry__range=(date_start, date_end)).order_by('-id')
        return_obj=ReturnDetails.objects.filter(date__range=(date_start, date_end)).order_by('-id')
        invoice_total_return=0
        total_spend=0
        updated_balance=0
        for i in inv_obj:
            total_spend += float(i.Total_Price())
        for j in return_obj:
            invoice_total_return += float(j.total_price_order)
            updated_balance=total_spend-invoice_total_return
        data={'invoices':inv_obj,"company": "Ritik Pharmacy Company",
	    "address": "123 Street name",
	    "city": "Durg",
	    "state": "C.G.",
	    "zipcode": "491001",
	    "phone": "1234567890",
	    "email": "pharma@bsuiness.com",
	    "website": "pharmacy.com"
        ,'return_hist':return_obj,
        'total_spend':total_spend,
        'updated_balance':updated_balance,
        'invoice_total_return':invoice_total_return
        }
        
        pdf = render_to_pdf('pdf_account.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
class DownloadPDF_accounts(View):
    def get(self, request, *args, **kwargs):
        date_start=request.session.get('date_start')
        date_end=request.session.get('date_end')
        inv_obj=Invoice.objects.filter(date_entry__range=(date_start, date_end)).order_by('-id')
        return_obj=ReturnDetails.objects.filter(date__range=(date_start, date_end)).order_by('-id')
        invoice_total_return=0
        total_spend=0
        updated_balance=0
        for i in inv_obj:
            total_spend += float(i.Total_Price())
        for j in return_obj:
            invoice_total_return += float(j.total_price_order)
            updated_balance=total_spend-invoice_total_return
        data={'invoices':inv_obj,"company": "Ritik Pharmacy Company",
	    "address": "123 Street name",
	    "city": "Durg",
	    "state": "C.G.",
	    "zipcode": "491001",
	    "phone": "1234567890",
	    "email": "pharma@bsuiness.com",
	    "website": "pharmacy.com"
        ,'return_hist':return_obj,
        'total_spend':total_spend,
        'updated_balance':updated_balance,
        'invoice_total_return':invoice_total_return
        }
        
        pdf = render_to_pdf('pdf_account.html', data)
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename=%s" %(filename)
        response['Content-Disposition'] = content
        return response