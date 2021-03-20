from django.urls import path
from . import views

app_name = 'vehicule'

urlpatterns = [

    # Brand urls
    path('brand_list', views.brand_list, name='brand_list'),
    path('add_brand', views.add_brand, name='add_brand'),
    path('update_brand/<str:pk>', views.update_brand, name='update_brand'),
    path('delete_brand/<str:pk>', views.delete_brand, name='delete_brand'),

    # type urls
    path('all_type_list/', views.all_type_list, name='all_type_list'),
    path('type_list/<str:pk>', views.type_list, name='type_list'),
    path('add_type', views.add_type, name='add_type'),
    path('add_type_rdv/<str:pk>', views.add_type_rdv, name='add_type_rdv'),
    path('update_type/<str:pk>', views.update_type, name='update_type'),
    path('delete_type/<str:pk>', views.delete_type, name='delete_type'),

    # Vehicle urls
    path('add_vehicule', views.add_vehicule, name='add_vehicule'),
    path('add_vehicule_rdv/<str:pk>', views.add_vehicule_rdv, name='add_vehicule_rdv'),
    path('all_vehicule_list/', views.all_vehicule_list, name='all_vehicule_list'),
    path('update_vehicule/<str:pk>', views.update_vehicule, name='update_vehicule'),
    path('delete_vehicule/<str:pk>', views.delete_vehicule, name='delete_vehicule'),
]
