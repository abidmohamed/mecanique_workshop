from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('all_product_list/', views.all_product_list, name='all_product_list'),
    # path('product_list/<str:pk>', views.product_list, name='product_list'),
    path('add_product', views.add_product, name='add_product'),
    path('delete_duplicated', views.delete_duplicated, name='delete_duplicated'),
    path('add_product_buyorder', views.add_product_buyorder, name='add_product_buyorder'),
    path('update_product/<str:pk>', views.update_product, name='update_product'),
    path('detail_product/<str:pk>', views.detail_product, name='detail_product'),
    path('delete_product/<str:pk>', views.delete_product, name='delete_product'),

]
