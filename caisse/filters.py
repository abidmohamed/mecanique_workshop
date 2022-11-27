import django_filters
from django_filters import CharFilter, DateFilter
from .models import *
from django import forms


class TransactionFilter(django_filters.FilterSet):
    name = CharFilter(field_name='Transaction_name', lookup_expr='icontains')
    start_date = DateFilter(field_name='trans_date', lookup_expr="gte",
                            widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = DateFilter(field_name='trans_date', lookup_expr="lte",
                          widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Transaction

        fields = ['name', 'category', 'Transaction_type', 'start_date', 'end_date']
