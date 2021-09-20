from django.forms import ModelForm, modelformset_factory
from django import forms
from payments.models import SellOrderPayment, CustomerCheque, BuyOrderPayment, SupplierCheque, ServicePayment


class CustomerPaymentForm(ModelForm):
    class Meta:
        model = SellOrderPayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['amount', 'pay_status', 'pay_date']


class CustomerChequeForm(ModelForm):
    class Meta:
        model = CustomerCheque

        fields = ['cheque_number', ]


class SupplierPaymentForm(ModelForm):
    class Meta:
        model = BuyOrderPayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['amount', 'pay_status', 'pay_date']


class SupplierChequeForm(ModelForm):
    class Meta:
        model = SupplierCheque

        fields = ['cheque_number', ]


class ServicePaymentForm(ModelForm):
    class Meta:
        model = ServicePayment
        widgets = {
            'pay_date': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }
        fields = ['amount', 'pay_date']
