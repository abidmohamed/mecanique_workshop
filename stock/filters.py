import django_filters
from django_filters import CharFilter
from .models import *


class StockProductFilter(django_filters.FilterSet):
    name = CharFilter(field_name='product__name', lookup_expr='icontains')
    ref = CharFilter(field_name='product__ref', lookup_expr='icontains')

    class Meta:
        model = StockProduct

        fields = ['name', 'stock']
