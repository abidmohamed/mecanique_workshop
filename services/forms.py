from django.forms import ModelForm, modelformset_factory
from services.models import ServiceProvider, Service


class ServiceProviderForm(ModelForm):
    class Meta:
        model = ServiceProvider

        fields = '__all__'


class ServiceForm(ModelForm):
    class Meta:
        model = Service

        fields = ['name', 'price', 'charge', ]
