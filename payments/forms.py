from django.forms import ModelForm, modelformset_factory

from payments.models import SellOrderPayment, CustomerCheque, BuyOrderPayment, SupplierCheque


class CustomerPaymentForm(ModelForm):
    class Meta:
        model = SellOrderPayment

        fields = ['amount', 'pay_status', ]


class CustomerChequeForm(ModelForm):
    class Meta:
        model = CustomerCheque

        fields = ['cheque_number',]


class SupplierPaymentForm(ModelForm):
    class Meta:
        model = BuyOrderPayment

        fields = ['amount', 'pay_status']


class SupplierChequeForm(ModelForm):
    class Meta:
        model = SupplierCheque

        fields = ['cheque_number',]