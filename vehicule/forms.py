from django.forms import ModelForm
from vehicule.models import *


class BrandForm(ModelForm):
    class Meta:
        model = Brand

        fields = ['name', 'image', ]


class TypeForm(ModelForm):
    class Meta:
        model = Type

        fields = ['brand', 'name', 'image', ]


class VehiculeFrom(ModelForm):
    class Meta:
        model = Vehicle

        fields = ['vehicle_name', 'vehicle_mat', 'vehicle_cart_gris']
