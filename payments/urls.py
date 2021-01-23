from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [

    path('create_customer_payment/<str:pk>', views.create_customer_payment, name='create_customer_payment'),
    path('create_customer_cheque/<str:pk>', views.create_customer_cheque, name='create_customer_cheque'),
    path('customer_payment_list', views.customer_payment_list, name='customer_payment_list'),

    path('create_supplier_payment/<str:pk>', views.create_supplier_payment, name='create_supplier_payment'),
    path('create_supplier_cheque/<str:pk>', views.create_supplier_cheque, name='create_supplier_cheque'),
    path('supplier_payment_list', views.supplier_payment_list, name='supplier_payment_list'),

]
