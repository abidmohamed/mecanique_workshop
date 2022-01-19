from django.db import models


# Create your models here.
class Caisse(models.Model):
    caisse_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    updated = models.DateTimeField(auto_now=True)


class CaisseHistory(models.Model):
    caisse_value = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


class TransactionCategory(models.Model):
    name = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name

    def get_total_cost(self):
        return round(sum(item.amount for item in self.items.all()), 2)


class Transaction(models.Model):
    Transaction_name = models.CharField(max_length=200, null=True)
    category = models.ForeignKey(TransactionCategory, on_delete=models.DO_NOTHING, null=True, blank=True,
                                 related_name="items")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )
    trans_date = models.DateField(null=True, blank=True)
    Transaction_type = models.CharField(max_length=8, choices=type_choices, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


