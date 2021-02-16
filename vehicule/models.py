from django.db import models
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.
from customer.models import Customer


class Brand(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='brands/%Y/%m/%d', blank=True, )

    class Meta:
        ordering = ('name',)
        verbose_name = 'brand'
        verbose_name_plural = 'brands'

    def __str__(self):
        return self.name

    # provides a category_slug parameter to the
    # view for filtering products according to a given category.
    def get_absolute_url(self):
        return reverse('vehicule:type_list', args=[self.id])


class Type(models.Model):
    brand = models.ForeignKey(Brand, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='types/%Y/%m/%d', blank=True,)

    class Meta:
        ordering = ('name',)
        verbose_name = 'type'
        verbose_name_plural = 'types'

    def __str__(self):
        return self.name

    # auto fill the slug when saving
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # if self.image:
        #    self.image = get_thumbnail(self.image, '570x320').url
        super(Type, self).save(*args, **kwargs)

    # def get_absolute_url(self):
    # TODO : Change it to the new url stock
    # return reverse('warehouse:stockproductcategory_list', args=[self.id])


class Vehicle(models.Model):
    vehicle_name = models.CharField(max_length=200, null=True)
    customer = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name="vehicles")
    vehicle_type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)
    vehicle_mat = models.CharField(max_length=200, null=True)
    vehicle_cart_gris = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.vehicle_name + " - " + self.vehicle_mat


class VehiculeHistory(models.Model):
    vehicle_name = models.CharField(max_length=200, null=True)
    customerOld = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='customerOld')
    customerNew = models.ForeignKey(Customer, null=True, on_delete=models.CASCADE, related_name='customerNew')
    vehicle_type = models.ForeignKey(Type, null=True, on_delete=models.CASCADE)
    vehicle_mat = models.CharField(max_length=200, null=True)
    vehicle_cart_gris = models.CharField(max_length=200, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.vehicle_name + " - " + self.vehicle_mat

