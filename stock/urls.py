from django.urls import path
from . import views

app_name = 'stock'

urlpatterns = [

    path('add_stock', views.add_stock, name='add_stock'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('all_stock_list', views.all_stock_list, name='all_stock_list'),
    path('update_stock/<str:pk>', views.update_stock, name='update_stock'),
    path('delete_stock/<str:pk>', views.delete_stock, name='delete_stock'),

    path('add_stockproduct', views.add_stockproduct, name='add_stockproduct'),
    path('stockproduct_list/<str:pk>', views.stockproduct_list, name='stockproduct_list'),
    path('all_stockproduct_list', views.all_stockproduct_list, name='all_stockproduct_list'),
    path('order_stockproduct_list', views.order_stockproduct_list, name='order_stockproduct_list'),
    path('modal_order_stockproduct_list/<str:pk>', views.modal_order_stockproduct_list,
         name='modal_order_stockproduct_list'),
    path('update_stockproduct/<str:pk>', views.update_stockproduct, name='update_stockproduct'),
    path('delete_stockproduct/<str:pk>', views.delete_stockproduct, name='delete_stockproduct'),
    path('stockproductcategory_list/<str:pk>', views.stockproductcategory_list, name='stockproductcategory_list'),
    path('stockproduct_detail/<str:id>', views.stockproduct_detail, name='stockproduct_detail'),
    path('order_vehicle/<str:pk>', views.order_vehicle, name='order_vehicle'),
    path('stockproduct_stockalert', views.stockproduct_quantityalert, name='stockproduct_stockalert'),

]
