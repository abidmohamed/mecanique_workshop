from django.urls import path
from . import views

app_name = 'supplier'

urlpatterns = [
    path('add_supplier', views.add_supplier, name='add_supplier'),
    path('supplier_list', views.supplier_list, name='supplier_list'),
    path('update_supplier/<str:pk>', views.update_supplier, name='update_supplier'),
    path('delete_supplier/<str:pk>', views.delete_supplier, name='delete_supplier'),

    path('supplier_detail/<str:pk>', views.supplier_detail, name='supplier_detail'),

    path('buyorder_supplier_list', views.buyorder_supplier_list, name='buyorder_supplier_list'),

]
