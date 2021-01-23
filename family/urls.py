from django.urls import path
from . import views

app_name = 'family'

urlpatterns = [

    path('family_list', views.family_list, name='family_list'),
    path('add_family', views.add_family, name='add_family'),
    path('update_family/<str:pk>', views.update_family, name='update_family'),
    path('delete_family/<str:pk>', views.delete_family, name='delete_family'),

]
