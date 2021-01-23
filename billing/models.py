from django.db import models

# Create your models here.
from buyorder.models import BuyOrder
from customer.models import Customer
from sellorder.models import Order
from supplier.models import Supplier


class BuyOrderBilling(models.Model):
    user = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Bill {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_weight(self):
        return sum(item.get_weight() for item in self.items.all())


class BillBuyOrderItem(models.Model):
    bill = models.ForeignKey(BuyOrderBilling, related_name='items', on_delete=models.CASCADE)
    order = models.ForeignKey(BuyOrder, related_name='orderbilling_item',
                              on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price

    def get_weight(self):
        return self.weight


# Sell Order Billing
class OrderBilling(models.Model):
    user = models.IntegerField(default=0)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Bill {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_weight(self):
        return sum(item.get_weight() for item in self.items.all())


class BillOrderItem(models.Model):
    bill = models.ForeignKey(OrderBilling, related_name='items', on_delete=models.CASCADE)
    order = models.ForeignKey(Order, related_name='orderbilling_item',
                              on_delete=models.CASCADE, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    weight = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0.0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price

    def get_weight(self):
        return self.weight
