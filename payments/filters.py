import django_filters
from django_filters import CharFilter, DateRangeFilter, DateFromToRangeFilter, DateFilter
from .models import *
from django import forms


class SupplierPaymentFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name='pay_date', lookup_expr="gte", widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='pay_date', lookup_expr="lte", widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = BuyOrderPayment

        fields = ['supplier', 'start_date', 'end_date', 'pay_status']
