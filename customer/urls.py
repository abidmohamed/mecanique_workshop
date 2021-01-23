from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('add_customer', views.add_customer, name='add_customer'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('customer_detail/<str:pk>', views.customer_detail, name='customer_detail'),
    path('delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),

    path('sellorder_customer_list', views.sellorder_customer_list, name='sellorder_customer_list'),

    path('add_city', views.add_city, name='add_city'),
    path('city_list', views.city_list, name='city_list'),
    path('update_city/<str:pk>', views.update_city, name='update_city'),
    path('delete_city/<str:pk>', views.delete_city, name='delete_city'),

]
