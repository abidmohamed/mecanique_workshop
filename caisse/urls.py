from django.urls import path
from . import views

app_name = 'caisse'

urlpatterns = [
    # Cash Regiter
    path('create_transaction/', views.create_transaction, name='create_transaction'),
    path('cash/', views.transaction_list, name='transaction_list'),
    # Transactions
    path('transaction_list/', views.in_out_transaction_list, name='in_out_transaction_list'),
    path('transaction_details/<str:pk>', views.transaction_details, name='transaction_details'),
    path('transaction_update/<str:pk>', views.transaction_update, name='transaction_update'),

    path('today_transaction_list/', views.today_transaction_list, name='today_transaction_list'),
    path('delete_transaction/<str:pk>', views.transaction_delete, name='transaction_delete'),

    # Category

    path('create_transaction_category/', views.create_transaction_category, name='create_transaction_category'),
    path('transaction_category_list/', views.transaction_category_list, name='transaction_category_list'),
    path('transaction_category_details/<str:pk>', views.transaction_category_details, name='transaction_category_details'),

]
