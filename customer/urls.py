from django.urls import path
from . import views

app_name = 'customer'

urlpatterns = [
    path('add_customer', views.add_customer, name='add_customer'),
    path('add_customer_rdv', views.add_customer_rdv, name='add_customer_rdv'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer_list_json', views.customer_list_json, name='customer_list_json'),
    path('customer_debt_list', views.customer_debt_list, name='customer_debt_list'),
    path('update_customer/<str:pk>', views.update_customer, name='update_customer'),
    path('customer_detail/<str:pk>', views.customer_detail, name='customer_detail'),
    path('delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),

    path('sellorder_customer_list', views.sellorder_customer_list, name='sellorder_customer_list'),
    path('proforma_customer_list', views.proforma_customer_list, name='proforma_customer_list'),

    path('add_city', views.add_city, name='add_city'),
    path('city_list', views.city_list, name='city_list'),
    path('update_city/<str:pk>', views.update_city, name='update_city'),
    path('delete_city/<str:pk>', views.delete_city, name='delete_city'),

    path('add_enterprise/<str:pk>', views.add_enterprise, name='add_enterprise'),
    path('update_enterprise/<str:pk>', views.update_enterprise, name='update_enterprise'),
    path('delete_enterprise/<str:pk>', views.delete_enterprise, name='delete_enterprise'),
    path('enterprise_list/', views.enterprise_list, name='enterprise_list'),

    path('add_avancement/<str:pk>', views.add_avancement, name='add_avancement'),

    # Old Debt Fixing
    path('old_dette_fix', views.old_dette_fix, name='old_dette_fix'),

    #########====> API's
    path('api/customer_list', views.ListCustomer.as_view(), name='api_customer_list'),

]
