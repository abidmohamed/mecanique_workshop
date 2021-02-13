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

]
