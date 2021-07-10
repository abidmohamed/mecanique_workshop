from django.urls import path
from . import views

app_name = 'buyorder'

urlpatterns = [

    path('create_buyorder', views.create_buyorder, name='create_buyorder'),
    path('buyorder_list', views.buyorder_list, name='buyorder_list'),
    path('buyorder_confirmation/<str:pk>', views.buyorder_confirmation, name='buyorder_confirmation'),
    path('buyorder_pdf/<str:pk>', views.buyorder_pdf, name='buyorder_pdf'),
    path('buyorder_details/<str:pk>', views.buyorder_details, name='buyorder_details'),
    path('buyorderorder_list_by_supplier/<str:pk>', views.buyorderorder_list_by_supplier, name='buyorderorder_list_by_supplier'),
    path('buyorder_delete/<str:pk>', views.buyorder_delete, name='buyorder_delete'),
    path('update_order/<str:pk>', views.update_order, name='update_order'),
    path('confirm_all', views.confirm_all, name='confirm_all'),

    path('confirm_order_item_delete/<str:orderpk>/<str:itempk>', views.confirm_order_item_delete,
         name='confirm_order_item_delete'),

]
