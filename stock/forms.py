from django.forms import ModelForm
from django import forms
from stock.models import Stock, StockProduct


class StockForm(ModelForm):
    class Meta:
        model = Stock

        fields = ['name']


class StockProductForm(ModelForm):
    class Meta:
        model = StockProduct

        fields = ['product', 'stock', 'quantity']
