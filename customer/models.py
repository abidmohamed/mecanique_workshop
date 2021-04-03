from django.db import models
from django.contrib.auth.models import User


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
    date_joined = models.DateField(null=True)
    enterprise = models.BooleanField(default=False)
    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return self.firstname + " " + self.lastname

    def get_vehicles(self):
        return self.vehicles.all().filter(customer=self)


class Enterprise(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='owner')
    rc = models.CharField(max_length=250, null=True)
    nif = models.CharField(max_length=250, null=True)
    nis = models.CharField(max_length=250, null=True)
    art = models.CharField(max_length=250, null=True)
