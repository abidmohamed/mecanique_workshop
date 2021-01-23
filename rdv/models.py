from django.db import models


# Create your models here.
from customer.models import Customer
from vehicule.models import Vehicle


class Rdv(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    rdv_date = models.DateField(null=True, blank=True)
    rdv_time = models.TimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    factured = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'RDV {self.id}'

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class Panne(models.Model):
    desc = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)


class RdvItem(models.Model):
    rdv = models.ForeignKey(Rdv, related_name='items', on_delete=models.CASCADE)
    panne = models.ForeignKey(Panne, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price


