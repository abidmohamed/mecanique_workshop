from django.db import models

# Create your models here.
from accounts.models import CurrentYear


class Supplier(models.Model):
    firstname = models.CharField(max_length=250, null=True)
    lastname = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_joined = models.DateField(null=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)

    def __str__(self):
        return self.firstname + " " + self.lastname

    def get_credit(self):
        total_credit = round(sum(order.debt for order in self.orders.filter(
            supplier=self,
            order_date__year=CurrentYear.objects.all().filter()[:1].get().year)
                                 ), 2)
        return total_credit
