from django.forms import ModelForm

from supplier.models import Supplier


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier

        fields = ('firstname', 'lastname', 'address', 'email', 'phone', 'credit')
