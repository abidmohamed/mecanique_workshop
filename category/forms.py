from django.forms import ModelForm
from django import forms

from category.models import Category
from family.models import Family


class CategoryForm(ModelForm):
    class Meta:
        model = Category

        fields = ['family', 'name', 'image', ]
