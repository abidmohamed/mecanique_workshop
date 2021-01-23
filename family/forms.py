from django.forms import ModelForm
from django import forms
from family.models import Family


class FamilyForm(ModelForm):
    class Meta:
        model = Family

        fields = ['name', 'image', ]
