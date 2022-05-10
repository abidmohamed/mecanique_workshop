import datetime

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, forms, TypedChoiceField

from accounts.models import CurrentYear


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']


def year_choices():
    return [(r, r) for r in range(2019, datetime.date.today().year + 50)]


class MyForm(ModelForm):
    year = TypedChoiceField(coerce=int, choices=year_choices, )


class CurrentYearForm(ModelForm):
    class Meta:
        model = CurrentYear
        fields = ['year', ]

    year = TypedChoiceField(coerce=int, choices=year_choices, )
