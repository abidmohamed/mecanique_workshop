from django.forms import ModelForm, modelformset_factory
from django import forms
from product.models import Product


class ProductForm(ModelForm):
    class Meta:
        model = Product

        fields = [
            # 'category',
            'brand', 'name', 'ref', 'desc', 'image', 'stock', 'sellprice',
            'buyprice',
        ]
