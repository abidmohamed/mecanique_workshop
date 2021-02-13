from django.forms import ModelForm
from django import forms
from discount.models import Discount


class DiscountForm(ModelForm):
    class Meta:
        model = Discount

        fields = ['value', 'discount_status', ]

        widgets = {

            'value': forms.NumberInput(attrs={"onkeyup": "calc()"}),
            'discount_status': forms.Select(attrs={"onkeyup": "calc()"}),
        }
