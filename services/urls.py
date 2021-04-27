from django.urls import path
from services import views

app_name = 'services'

urlpatterns = [

    path('add_service', views.add_service, name='add_service'),
    path('service_list', views.service_list, name='service_list'),
    path('update_service/<str:pk>', views.update_service, name='update_service'),
    path('delete_service/<str:pk>', views.delete_service, name='delete_service'),

    path('add_provider', views.add_provider, name='add_provider'),
    path('provider_list', views.provider_list, name='provider_list'),
    path('update_provider/<str:pk>', views.update_provider, name='update_provider'),
    path('delete_provider/<str:pk>', views.delete_provider, name='delete_provider'),

]


