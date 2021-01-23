from django.urls import path
from . import views

app_name = 'billing'

urlpatterns = [

    path('buybill_list', views.buybill_list, name='buybill_list'),
    path('buybill_pdf/<str:pk>', views.buybill_pdf, name='buybill_pdf'),

    path('sellbill_list', views.sellbill_list, name='sellbill_list'),
    path('sellbill_pdf/<str:pk>', views.sellbill_pdf, name='sellbill_pdf'),

]
