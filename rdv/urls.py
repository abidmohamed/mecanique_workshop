from django.urls import path
from . import views

app_name = 'rdv'

urlpatterns = [

    path('create_rdv_customer', views.create_rdv_customer, name='create_rdv_customer'),
    path('rdv_vehicle_list/<str:pk>', views.rdv_vehicle_list, name='rdv_vehicle_list'),
    path('rdv_list', views.rdv_list, name='rdv_list'),
    path('create_rdv/<str:pk>', views.create_rdv, name='create_rdv'),
    path('rdv_pdf/<str:pk>', views.rdv_pdf, name='rdv_pdf'),
    path('rdv_details/<str:pk>', views.rdv_details, name='rdv_details'),

    # Panne
    path('create_panne', views.create_panne, name='create_panne'),
    path('panne_list', views.panne_list, name='panne_list'),
    path('update_panne/<str:pk>', views.update_panne, name='update_panne'),
    path('delete_panne/<str:pk>', views.delete_panne, name='delete_panne'),

]
