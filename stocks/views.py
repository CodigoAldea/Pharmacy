from django.shortcuts import render
from .models import *
# Create your views here.
def stocks_home(request):
    medicine=Stocks.objects.all()
    less=Stocks.objects.filter(quantity__lt=20)
    expired=[obj for obj in medicine if obj.is_expired()]
    return render(request,'stocks/stocks.html',{'stock':medicine,'less':less,'expired':expired})