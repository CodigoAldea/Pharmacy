"""
URL configuration for Pharmacy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path,include
# from .views import *
from admin_user import urls as admin_url
from medicine import urls as medicine_url
from purchase import urls as purchase_url
from pos import urls as pos_url
from stocks import urls as stocks_url
from supplier import urls as supplier_url
from accounts import urls as accounts_url
from django.conf import settings
from django.conf.urls.static import static
# from .views import custom_404

# handler404 = custom_404

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include(admin_url)),
    path('',include(medicine_url)),
    path('',include(purchase_url)),
    path('',include(pos_url)),
    path('',include(stocks_url)),
    path('',include(supplier_url)),
    path('',include(accounts_url)),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)