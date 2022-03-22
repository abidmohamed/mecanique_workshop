import django_filters
from django_filters import CharFilter
from .models import *


class CustomerFilter(django_filters.FilterSet):
    firstname = CharFilter(field_name='firstname', lookup_expr='icontains')
    lastname = CharFilter(field_name='lastname', lookup_expr='icontains')
    phone = CharFilter(field_name='phone', lookup_expr='icontains')

    class Meta:
        model = Customer

        fields = ['id', 'firstname', 'lastname', 'phone', 'enterprise']

