from django.urls import path
from . import views

app_name = 'caisse'

urlpatterns = [

    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('transaction_list/', views.transaction_list, name='transaction_list'),

]
