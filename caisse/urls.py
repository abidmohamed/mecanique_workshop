from django.urls import path
from . import views

app_name = 'caisse'

urlpatterns = [

    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),
    path('today_transaction_list/', views.today_transaction_list, name='today_transaction_list'),
    path('delete_transaction/<str:pk>', views.delete_transaction, name='delete_transaction'),

]
