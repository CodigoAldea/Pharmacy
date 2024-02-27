from django.urls import path,include
from .views import *
urlpatterns = [
    path('pos',pos_home,name='pos_home'),
      # path('live_search/', live_search, name='live_search'),
    path('return',return_home,name='return_home'),
    path('return_details',return_details,name='return_details'),
    path('return_purchase',return_purchase,name='return_purchase'),
    path('delete_stock/<int:stock_id>',delete_stock,name='delete_stock'),
    path('test/', test),
    path('pdf_view/', ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', DownloadPDF.as_view(), name="pdf_download"),
    path('delete_order/<int:ord_id>', delete_order,name='delete_order'),
    path('delete_invoice/<int:ord_id>', delete_invoice,name='delete_invoice'),
    path('invoice_relocate/<int:inv_id>', invocie_relocate,name='invoice_relocate'),
     path('fetch-data-from-database', fetch_data_from_database, name='fetch-data-from-database'),
     path('fetch-batch-ids/', fetch_batch_ids, name='fetch_batch_ids'),
     path('update_order/', update_order, name='update_order'),
     
]
