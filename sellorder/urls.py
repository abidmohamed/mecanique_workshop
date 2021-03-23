from django.urls import path
from . import views

app_name = 'sellorder'

urlpatterns = [

    path('sellorder_list', views.sellorder_list, name='sellorder_list'),
    path('facture_all', views.facture_all, name='facture_all'),
    path('performa_sellorder_list', views.performa_sellorder_list, name='performa_sellorder_list'),
    path('factured_sellorder_list', views.factured_sellorder_list, name='factured_sellorder_list'),
    path('confirm_order_performa/<str:pk>', views.confirm_order_performa, name='confirm_order_performa'),
    path('confirm_order/<str:pk>', views.confirm_order, name='confirm_order'),
    path('sellorder_facture/<str:pk>', views.sellorder_facture, name='sellorder_facture'),
    path('sellorder_list_by_customer/<str:pk>', views.sellorder_list_by_customer,
         name='sellorder_list_by_customer'),
    path('sellorder_pdf/<str:pk>', views.sellorder_pdf, name='sellorder_pdf'),
    path('sellorder_details/<str:pk>', views.sellorder_details, name='sellorder_details'),
    path('sellorder_delete/<str:pk>', views.sellorder_delete, name='sellorder_delete'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('order_item_delete/<str:orderpk>/<str:itempk>', views.order_item_delete, name='order_item_delete'),
    path('get_orders_pannes', views.get_orders_pannes, name='get_orders_pannes'),
    path('get_orders_pieces', views.get_orders_pieces, name='get_orders_pieces'),

]
