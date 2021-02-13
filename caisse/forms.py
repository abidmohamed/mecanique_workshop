from django.forms import ModelForm
from django import forms

from caisse.models import Transaction


class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        widgets = {
            'trans_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['Transaction_name', 'amount', 'Transaction_type', 'trans_date']

