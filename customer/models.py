from django.db import models
from django.contrib.auth.models import User


class City(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=250, null=True)
    lastname = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    national_number = models.CharField(max_length=200, null=True)
    email = models.EmailField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_joined = models.DateField(null=True)

    debt = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def __str__(self):
        return self.firstname + " " + self.lastname
