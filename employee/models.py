from django.db import models


# Create your models here.
class Job(models.Model):
    name = models.CharField(max_length=250, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Employee(models.Model):
    job = models.ForeignKey(Job, on_delete=models.DO_NOTHING, null=True, blank=True)
    firstname = models.CharField(max_length=250, null=True)
    lastname = models.CharField(max_length=250, null=True)
    address = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_joined = models.DateField(null=True)
    weekly_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0)

    def __str__(self):
        return self.firstname + " " + self.lastname
