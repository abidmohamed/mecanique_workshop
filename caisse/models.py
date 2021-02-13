from django.db import models


# Create your models here.
class Caisse(models.Model):
    caisse_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated = models.DateTimeField(auto_now=True)


class CaisseHistory(models.Model):
    caisse_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class Transaction(models.Model):
    Transaction_name = models.CharField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    type_choices = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )
    trans_date = models.DateField(null=True, blank=True)
    Transaction_type = models.CharField(max_length=8, choices=type_choices, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
