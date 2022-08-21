import django_filters
from django_filters import CharFilter
from .models import *


class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product

        fields = ['brand', 'name', 'ref']
