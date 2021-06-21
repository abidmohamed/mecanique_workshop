from django.forms import ModelForm
from django import forms

from bank.models import BankTransaction


class BankTransactionForm(ModelForm):
    class Meta:
        model = BankTransaction
        widgets = {
            'trans_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['Transaction_name', 'amount', 'Transaction_type', 'trans_date', 'cheque_number']
