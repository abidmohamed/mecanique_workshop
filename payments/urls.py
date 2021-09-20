from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    # Customer
    path('create_customer_payment/<str:pk>', views.create_customer_payment, name='create_customer_payment'),
    path('create_customer_cheque/<str:pk>', views.create_customer_cheque, name='create_customer_cheque'),
    path('delete_customer_payment/<str:pk>', views.delete_customer_payment, name='delete_customer_payment'),
    path('customer_payment_list', views.customer_payment_list, name='customer_payment_list'),

    # Supplier
    path('create_supplier_payment/<str:pk>', views.create_supplier_payment, name='create_supplier_payment'),
    path('create_supplier_payment_by_supplier/<str:pk>', views.create_supplier_payment_by_supplier, name='create_supplier_payment_by_supplier'),
    path('create_supplier_cheque/<str:pk>', views.create_supplier_cheque, name='create_supplier_cheque'),
    path('supplier_payment_list', views.supplier_payment_list, name='supplier_payment_list'),
    path('delete_supplier_payment/<str:pk>', views.delete_supplier_payment, name='delete_supplier_payment'),

    # Service
    path('create_service_payment/<str:pk>', views.create_service_payment, name='create_service_payment'),
    path('service_payment_list', views.service_payment_list, name='service_payment_list'),

]
