from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # path('login/', views.loginpage, name='login'),
    # path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),

]
