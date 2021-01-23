from django.db import models
from customer.models import Customer
from supplier.models import Supplier


# Create your models here.
class CustomerPayment(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    user = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    pay_type = (
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    )
    pay_status = models.CharField(max_length=8, choices=pay_type, blank=True, default="Cash")


class CustomerCheque(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    customerpayment = models.ForeignKey(CustomerPayment, on_delete=models.CASCADE, null=True)
    cheque_number = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class SupplierPayment(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    user = models.IntegerField(default=0)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)
    pay_type = (
        ('Cash', 'Cash'),
        ('Cheque', 'Cheque'),
    )
    pay_status = models.CharField(max_length=8, choices=pay_type, blank=True, default="Cash")


class SupplierCheque(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    supplierpayment = models.ForeignKey(SupplierPayment, on_delete=models.CASCADE, null=True)
    cheque_number = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
