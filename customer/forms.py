from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm

from customer.models import Customer, City, Enterprise, Avancements


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

        fields = ('firstname', 'lastname', 'address', 'phone', 'enterprise', 'debt')


class EnterpriseForm(ModelForm):
    class Meta:
        model = Enterprise

        fields = ('nif', 'nif_check', 'nis', 'nis_check', 'art', 'art_check', 'rc', 'rc_check', 'article_imposition', 'ai_check',
                  'N_compte', 'matriculation')


class AvancementForm(ModelForm):
    class Meta:
        model = Avancements

        fields = ('number', 'amount')
