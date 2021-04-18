from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'accounts'

urlpatterns = [
    # path('login/', views.loginpage, name='login'),
    # path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('serviceworker', (TemplateView.as_view(
        template_name="serviceworker.js",
        content_type='application/javascript', )),
         name='serviceworker'),

]
