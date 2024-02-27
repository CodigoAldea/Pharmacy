from .views import *
from django.urls import path

urlpatterns = [
    path('purchase',purchase_home,name='purchase_home'),
    #  path('export/', export_data, name='export_data'),
    path('imp', import_file, name='import_file'),
    path('purchase/purchase_history',purchase_history,name='purchase_history'),
    # path('imp',import_home,name='import_home'),

]
