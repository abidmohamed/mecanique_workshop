from django.db import models
from category.models import Category


# Create your models here.
class Product(models.Model):
    # add buy price or production price
    # category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    brand = models.CharField(max_length=250, null=True)
    name = models.CharField(max_length=250, null=True)
    ref = models.CharField(max_length=250, null=True)
    desc = models.CharField(max_length=250, null=True, blank=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, )
    buyprice = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    sellprice = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    # sellpricesemi_grou = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    # sellpricegrou = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    # sellspecialprice = models.DecimalField(max_digits=10, null=True, decimal_places=2, default=0)
    alert_quantity = models.PositiveIntegerField(default=1, blank=True, null=True)
    # box_quantity = models.PositiveIntegerField(default=1)
    stock = models.ForeignKey('stock.Stock', blank=False, null=False, on_delete=models.CASCADE, default=1)

    class Meta:
        ordering = ('name',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def __str__(self):
        return self.name

