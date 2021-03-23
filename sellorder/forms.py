from django.forms import ModelForm
from django import forms


class PeriodForm(forms.Form):
    start_date = forms.DateTimeField(initial="2021-01-01",
                                     widget=forms.DateInput(attrs={
                                         'class': 'form-control datepicker', 'type': 'date'
                                     })
                                     )
    end_date = forms.DateTimeField(initial="2021-01-01",
                                   widget=forms.DateInput(attrs={
                                       'class': 'form-control datepicker', 'type': 'date'
                                   })
                                   )
