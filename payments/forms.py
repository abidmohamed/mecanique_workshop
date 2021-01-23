from django.forms import ModelForm, modelformset_factory

from payments.models import CustomerPayment, CustomerCheque, SupplierPayment, SupplierCheque


class CustomerPaymentForm(ModelForm):
    class Meta:
        model = CustomerPayment

        fields = ['amount', 'pay_status', ]


class CustomerChequeForm(ModelForm):
    class Meta:
        model = CustomerCheque

        fields = ['cheque_number',]


class SupplierPaymentForm(ModelForm):
    class Meta:
        model = SupplierPayment

        fields = ['amount', 'pay_status']


class SupplierChequeForm(ModelForm):
    class Meta:
        model = SupplierCheque

        fields = ['cheque_number',]