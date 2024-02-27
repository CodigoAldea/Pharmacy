from django.urls import path
from .views import *

urlpatterns = [
    path('supplier',supplier_home,name='supplier_home')
]
