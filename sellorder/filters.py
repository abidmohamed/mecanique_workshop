import django_filters
from django_filters import CharFilter, DateRangeFilter
from .models import *


class SellorderFilter(django_filters.FilterSet):
    firstname = CharFilter(field_name='customer__firstname', lookup_expr='icontains')
    lastname = CharFilter(field_name='customer__lastname', lookup_expr='icontains')
    date_range = DateRangeFilter(field_name='order_date')

    class Meta:
        model= Order

        fields = ['firstname', 'lastname', 'date_range']