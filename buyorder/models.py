from decimal import Decimal

from django.db import models
from product.models import Product
from stock.models import Stock
from supplier.models import Supplier


# Create your models here.

class BuyOrder(models.Model):
    user = models.IntegerField(default=0)
    supplier = models.ForeignKey(Supplier, on_delete=models.DO_NOTHING, related_name="orders")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    order_tva = models.PositiveIntegerField(default=0)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)
    confirmed = models.BooleanField(default=False)
    order_date = models.DateField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=0)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Order {self.id}'

    def get_total_cost(self):
        return round(sum(item.get_cost() for item in self.items.all()), 2)

    def get_tva(self):
        return round(self.get_total_cost() * Decimal(self.order_tva/100), 2)

    def get_ttc(self):
        return round(self.get_total_cost() + self.get_tva(), 2)


class BuyOrderItem(models.Model):
    order = models.ForeignKey(BuyOrder,
                              related_name='items',
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
                                related_name='buyorder_item',
                                on_delete=models.DO_NOTHING, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.ForeignKey(Stock, related_name='item_stocks', on_delete=models.DO_NOTHING, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return round(self.price * self.quantity, 2)
