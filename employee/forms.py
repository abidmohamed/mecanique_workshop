from django.forms import ModelForm
from django import forms
from employee.models import Job, Employee


class JobForm(ModelForm):
    class Meta:
        model = Job
        fields = ('name',)


class EmployeeForm(ModelForm):
    class Meta:
        model = Employee

        widgets = {
            'date_joined': forms.DateInput(attrs={'class': 'datepicker', 'type': 'date'}),
        }

        fields = ('firstname', 'lastname', 'address', 'phone', 'job', 'weekly_salary', 'date_joined')

