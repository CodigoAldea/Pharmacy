from .views import *
from django.urls import path

urlpatterns = [
    path('medicine',medicine_home,name='medicine_home'),

]
