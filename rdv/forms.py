from django.forms import ModelForm, modelformset_factory
from django import forms

from rdv.models import Rdv, Panne


class RdvFrom(ModelForm):
    class Meta:
        model = Rdv
        widgets = {
            'rdv_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
            'rdv_time': forms.TimeInput(attrs={'class': 'timepicker', 'type': 'time'})
        }
        fields = ['rdv_date', 'rdv_time', ]


class PanneForm(ModelForm):
    class Meta:
        model = Panne
        fields = ['desc', 'price']
