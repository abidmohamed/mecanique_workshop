from django.db import models

# Create your models here.
from accounts.models import CurrentYear


class ServiceProvider(models.Model):
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    credit = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.0)

    def __str__(self):
        return self.name

    def get_credit(self):
        if self.id == 18:
            real_credit = 0
        else:
            total_credit = round(sum(item.price for item in self.provided_item.filter(
                provider=self,
                order__confirmed=True,
                order__order_date__year=CurrentYear.objects.all().filter()[:1].get().year
            )), 2)
            total_payment = round(sum(payment.amount for payment in self.payments.filter(
                provider=self,
                pay_date__year=CurrentYear.objects.all().filter()[:1].get().year
            )), 2)

            real_credit = total_credit - total_payment
            # print(total_payment)
            # print(total_credit)
        self.credit = real_credit
        return real_credit


class Service(models.Model):
    name = models.CharField(max_length=200, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    charge = models.DecimalField(max_digits=10, decimal_places=2)
    provider = models.ForeignKey(ServiceProvider, on_delete=models.DO_NOTHING, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_total(self):
        return self.price + self.charge
