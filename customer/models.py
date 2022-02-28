from django.db import models
from django.contrib.auth.models import User

from accounts.models import CurrentYear


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=250, null=True)
    lastname = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    # national_number = models.CharField(max_length=200, null=True)
    # email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateField(null=True)
    enterprise = models.BooleanField(default=False)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return self.firstname + " " + self.lastname

    def get_vehicles(self):
        return self.vehicles.all().filter(customer=self)

    def get_debt(self):
        self.debt = round(sum(order.debt for order in self.orders.filter(
            customer=self,
            confirmed=True,
            order_date__year=CurrentYear.objects.all().filter()[:1].get().year)
                         ), 2)
        return round(sum(order.debt for order in self.orders.filter(
            customer=self,
            confirmed=True,
            order_date__year=CurrentYear.objects.all().filter()[:1].get().year)
                         ), 2)

    def save(self, *args, **kwargs):
        self.debt = self.get_debt()


class Enterprise(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='owner')
    rc = models.CharField(max_length=250, null=True, blank=True)
    rc_check = models.BooleanField(default=False)
    nif = models.CharField(max_length=250, null=True, blank=True)
    nif_check = models.BooleanField(default=False)
    nis = models.CharField(max_length=250, null=True, blank=True)
    nis_check = models.BooleanField(default=False)
    art = models.CharField(max_length=250, null=True, blank=True)
    art_check = models.BooleanField(default=False)
    article_imposition = models.CharField(max_length=250, null=True, blank=True)
    ai_check = models.BooleanField(default=False)
    matriculation = models.BooleanField(default=False)
    N_compte = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.customer.__str__()


class Avancements(models.Model):
    number = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='avancement')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='all_avancement')
    amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)
