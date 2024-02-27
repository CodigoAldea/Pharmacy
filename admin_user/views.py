from django.shortcuts import render
from pos.models import *
from stocks.models import *
from datetime import datetime, timedelta


# Create your views here.
def adm_home(request):
    order_obj=Order.objects.all()
    pos_obj=POS.objects.all()
    invoice_obj=Invoice.objects.all()
    invoice_recent=Invoice.objects.all().order_by('-id')[:4]
    stocks_obj=Stocks.objects.filter()
    expired=[obj for obj in stocks_obj if obj.is_expired()]
    total_price = (int(item.Total_Price()) for item in invoice_obj)
    sum_inv=(sum(total_price))
    # Calculate the date 7 days ago from today
    current_date=datetime.now()
    seven_days_ago = datetime.now() - timedelta(days=7)
    one_month_ago = datetime.now() - timedelta(days=30)
    one_year_ago = datetime.now() - timedelta(days=365)
    
    current_year=datetime.now().year
    current_month=datetime.now().month
    start_date_year = datetime(current_year, 1, 1)
    end_date_year = datetime(current_year, 12, 31, 23, 59, 59)
    start_date_month = datetime(current_year, current_month, 1)
    
    last_day_of_month = 28  # Default for February
    if current_month in [1, 3, 5, 7, 8, 10, 12]:
        last_day_of_month = 31
    elif current_month in [4, 6, 9, 11]:
        last_day_of_month = 30
    end_date_month = datetime(current_year, current_month, last_day_of_month, 23, 59, 59)
    start_date_week = current_date - timedelta(days=current_date.weekday())
    end_date_week = start_date_week + timedelta(days=6)

    # Query objects with a date within the last 7 days
    # invoice_last_7_days = Invoice.objects.filter(date_entry__range=(seven_days_ago, datetime.now())) For Last 7 days
    invoice_last_7_days = Invoice.objects.filter(date_entry__range=(start_date_week, end_date_week))  #For weekly
    invoice_last_7_days_revenue = (int(item.Total_Price()) for item in invoice_last_7_days) 
    revenue_7days_sum=sum(invoice_last_7_days_revenue)
    # order_7_days=POS.objects.filter(date_entry__range=(seven_days_ago, datetime.now())) For last 7 days
    order_7_days=POS.objects.filter(date_entry__range=(start_date_week, end_date_week)) #For weekly
    
    # invoice_last_30_days = Invoice.objects.filter(date_entry__range=(one_month_ago, datetime.now())) For last 30 days
    invoice_last_30_days = Invoice.objects.filter(date_entry__range=(start_date_month, end_date_month)) # for current month sales
    invoice_last_30_days_revenue = (int(item.Total_Price()) for item in invoice_last_30_days)
    revenue_30days_sum=sum(invoice_last_30_days_revenue)
    # order_one_month=POS.objects.filter(date_entry__range=(one_month_ago, datetime.now())) For last 30 days
    order_one_month=POS.objects.filter(date_entry__range=(start_date_month, end_date_month)) #For current month
    
    # invoice_last_1_year = Invoice.objects.filter(date_entry__range=(one_year_ago, datetime.now())) For Last 365 days
    invoice_last_1_year = Invoice.objects.filter(date_entry__range=(start_date_year, end_date_year)) #For current Year
    invoice_last_1_year_revenue = (int(item.Total_Price()) for item in invoice_last_1_year)
    revenue_1_year_sum=sum(invoice_last_1_year_revenue)
    # order_one_year=POS.objects.filter(date_entry__range=(one_year_ago, datetime.now())) For Last 365 days
    order_one_year=POS.objects.filter(date_entry__range=(start_date_year, end_date_year)) #For current Year
    
    order_daily=POS.objects.filter(date_entry=datetime.now())
    invoice_daily=Invoice.objects.filter(date_entry=datetime.now())
    invoice_daily_list=(int(item.Total_Price()) for item in invoice_daily)
    invoice_daily_sum=sum(invoice_daily_list)
    
    
    cust_obj=Customer.objects.all()
    cust_count=len(cust_obj)
    
    context={'order_info':order_obj,
             'invoice_info':invoice_obj,
             'invoice_recent':invoice_recent,
             'sum_inv':sum_inv,
             'days_7_revenue':revenue_7days_sum,
             'one_year_revenue':revenue_1_year_sum,
             'one_month_revenue':revenue_30days_sum,
             'order_7_days':order_7_days,
             'order_one_month':order_one_month,
             'order_one_year':order_one_year,
             'order_daily':order_daily,
             'invoice_daily_sum':invoice_daily_sum,
             'cust_count':cust_count,
             'pos_info':pos_obj ,
             'expired':expired,
             'current_date':current_date}
    return render(request,'index.html',context)
