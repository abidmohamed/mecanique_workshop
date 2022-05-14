from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'accounts'

urlpatterns = [
    # auths
    path('accounts/login/', views.loginpage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    # Dashboard
    path('', views.home, name='home'),

    # User
    path('add_user/', views.add_user, name='add_user'),
    path('users_list/', views.users_list, name='users_list'),
    path('update_user/<str:pk>', views.update_user, name='update_user'),


    # Offline Service Worker
    path('serviceworker', (TemplateView.as_view(
        template_name="serviceworker.js",
        content_type='application/javascript', )),
         name='serviceworker'),

    # year choosing
    path('choose_the_year/', views.choose_the_year, name='choose_the_year'),

]
