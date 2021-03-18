from decimal import Decimal
from unicodedata import decimal

from django.db import models

# Create your models here.
from customer.models import Customer
from rdv.models import Panne
from stock.models import StockProduct
from vehicule.models import Vehicle


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    paid = models.BooleanField(default=False)
    order_tva = models.PositiveIntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def get_total_panne(self):
        return sum(item.get_cost() for item in self.pannes.all())

    def get_total_item_panne(self):
        return sum(item.get_cost() for item in self.pannes.all()) + sum(item.get_cost() for item in self.items.all())

    def get_tva(self):
        return round(self.get_total_item_panne() * Decimal(self.order_tva/100), 2)

    def get_ttc(self):
        return round(self.get_total_item_panne() + self.get_tva() - self.discount_amount, 2)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    stockproduct = models.ForeignKey(StockProduct,
                                     related_name='order_item',
                                     on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class PanneItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='pannes',
                              on_delete=models.CASCADE)
    panne = models.ForeignKey(Panne, related_name='order_panne',
                              on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price
