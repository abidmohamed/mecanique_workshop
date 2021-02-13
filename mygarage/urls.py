"""mygarage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, include

from mygarage import settings

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    # the main ressource
    path('', include('accounts.urls', namespace='accounts')),
    path('customer/', include('customer.urls', namespace='customer')),
    path('supplier/', include('supplier.urls', namespace='supplier')),
    path('payments/', include('payments.urls', namespace='payments')),
    path('family/', include('family.urls', namespace='family')),
    path('category/', include('category.urls', namespace='category')),
    path('stock/', include('stock.urls', namespace='stock')),
    path('product/', include('product.urls', namespace='product')),
    path('buyorder/', include('buyorder.urls', namespace='buyorder')),
    path('sellorder/', include('sellorder.urls', namespace='sellorder')),
    path('billing/', include('billing.urls', namespace='billing')),
    path('vehicule/', include('vehicule.urls', namespace='vehicule')),
    path('rdv/', include('rdv.urls', namespace='rdv')),
    path('caisse/', include('caisse.urls', namespace='caisse')),
    # path('discount/', include('discount.urls', namespace='discount')),

    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

