from django.urls import path
from . import views

app_name = 'category'

urlpatterns = [

    path('all_category_list/', views.all_category_list, name='all_category_list'),
    path('category_list/<str:pk>', views.category_list, name='category_list'),
    path('add_category', views.add_category, name='add_category'),
    path('update_category/<str:pk>', views.update_category, name='update_category'),
    path('delete_category/<str:pk>', views.delete_category, name='delete_category'),

]
