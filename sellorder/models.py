import decimal
from decimal import Decimal
from unicodedata import decimal

from django.db import models

# Create your models here.
from customer.models import Customer
from rdv.models import Panne
from services.models import Service, ServiceProvider
from stock.models import StockProduct
from vehicule.models import Vehicle


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.DO_NOTHING, related_name="orders")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.DO_NOTHING, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    timbre = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    paid = models.BooleanField(default=False)
    order_tva = models.PositiveIntegerField(default=0)
    confirmed = models.BooleanField(default=False)
    factured = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return round(sum(item.get_cost() for item in self.items.all()), 2)

    def get_total_benefit(self):
        return round(sum(item.get_benefit() for item in self.items.all()), 2)

    def get_total_panne(self):
        return round(sum(item.get_cost() for item in self.pannes.all()), 2)

    def get_total_service(self):
        return round(sum(item.get_cost() for item in self.services.all()), 2)

    def get_total_item_panne(self):
        return round(sum(item.get_cost() for item in self.pannes.all()) + self.get_total_cost() + \
                     sum(item.get_cost() for item in self.services.all()), 2)

    def get_tva(self):
        return round(self.get_total_item_panne() * Decimal(self.order_tva / 100), 2)

    def get_ttc(self):
        return round(self.get_total_item_panne() + self.get_tva() - self.discount_amount + self.timbre, 2)

    def get_debt(self):
        return self.debt


class OrderItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='items',
                              on_delete=models.CASCADE)
    stockproduct = models.ForeignKey(StockProduct,
                                     related_name='order_item',
                                     on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return round(self.price * self.quantity, 2)

    def get_benefit(self):
        if self.stockproduct.product:
            return round((self.price - self.stockproduct.product.buyprice) * self.quantity, 2)
        else:
            return 0


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


class ServiceItem(models.Model):
    order = models.ForeignKey(Order,
                              related_name='services',
                              on_delete=models.CASCADE)
    service = models.ForeignKey(Service, related_name='order_service',
                                on_delete=models.DO_NOTHING, null=True, blank=True)
    provider = models.ForeignKey(ServiceProvider, related_name='provided_item',
                                 on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, default=0)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return Decimal(self.price) + Decimal(0 if self.charge is None else self.charge)


# Facture
class SellOrderFacture(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
