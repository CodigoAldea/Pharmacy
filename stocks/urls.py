from .views import *
from django.urls import path

urlpatterns = [
    path('stocks',stocks_home,name='stocks_home'),

]
