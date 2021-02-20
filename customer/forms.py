from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from customer.models import Customer, City


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ('name',)


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


class CustomerForm(ModelForm):
    class Meta:
        model = Customer

        widgets = {

        }

        fields = ('firstname', 'lastname', 'address', 'phone', 'debt')
