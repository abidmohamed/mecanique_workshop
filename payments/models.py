from django.db import models

from buyorder.models import BuyOrder
from customer.models import Customer
from sellorder.models import Order
from supplier.models import Supplier


# Create your models here.
class SellOrderPayment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True)
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
    sellorderpayment = models.ForeignKey(SellOrderPayment, on_delete=models.CASCADE, null=True)
    cheque_number = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)


class BuyOrderPayment(models.Model):
    order = models.ForeignKey(BuyOrder, on_delete=models.CASCADE, blank=True, null=True)
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
    buyorderpayment = models.ForeignKey(BuyOrderPayment, on_delete=models.CASCADE, null=True)
    cheque_number = models.PositiveIntegerField()
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True)
