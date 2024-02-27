from .views import *
from django.urls import path

urlpatterns = [
    path('accounts',accounts_home,name='accounts_home'),
    path('accounts/customer',account_cust,name='customer'),
    path('pdf_view_account/', ViewPDF_accounts.as_view(), name="pdf_view_account"),
    path('pdf_download_account/', DownloadPDF_accounts.as_view(), name="pdf_download_account"),

]
