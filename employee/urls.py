from django.urls import path
from . import views

app_name = 'employee'

urlpatterns = [
    # jobs
    path('add_job', views.add_job, name='add_job'),
    path('list_job', views.list_job, name='list_job'),

    # employee
    path('add_employee', views.add_employee, name='add_employee'),
    path('list_employee', views.list_employee, name='list_employee'),
    path('update_employee/<str:pk>', views.update_employee, name='update_employee'),
    path('delete_employee/<str:pk>', views.delete_employee, name='delete_employee'),

]