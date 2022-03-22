import django_filters
from django_filters import CharFilter
from .models import *


class PanneFilter(django_filters.FilterSet):
    desc = CharFilter(field_name='desc', lookup_expr='icontains')

    class Meta:
        model = Panne

        fields = ['desc', 'price']