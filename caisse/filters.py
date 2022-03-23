import django_filters
from django_filters import CharFilter
from .models import *


class TransactionFilter(django_filters.FilterSet):
    name = CharFilter(field_name='Transaction_name', lookup_expr='icontains')

    class Meta:
        model = Transaction

        fields = ['name', 'category', 'Transaction_type']
