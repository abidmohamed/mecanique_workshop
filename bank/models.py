from django.db import models


# Create your models here.
class BankTransaction(models.Model):
    Transaction_name = models.CharField(max_length=200, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type_choices = (
        ('Income', 'Income'),
        ('Expense', 'Expense')
    )
    trans_date = models.DateField(null=True, blank=True)
    cheque_number = models.PositiveIntegerField()
    Transaction_type = models.CharField(max_length=8, choices=type_choices, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ('trans_date',)
