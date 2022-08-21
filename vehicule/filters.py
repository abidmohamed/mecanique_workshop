import django_filters
from django_filters import CharFilter
from .models import *


class VehicleFilter(django_filters.FilterSet):

    class Meta:
        model = Vehicle

        fields = ['vehicle_name', 'vehicle_type', 'vehicle_mat']
