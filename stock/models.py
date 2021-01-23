from django.db import models


# Create your models here.
from category.models import Category
from product.models import Product


class Stock(models.Model):
    name = models.CharField(max_length=250, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'stock'
        verbose_name_plural = 'stocks'

    def __str__(self):
        return self.name


class StockProduct(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    stock = models.ForeignKey(Stock, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ('product',)
        verbose_name = 'stockproduct'
        verbose_name_plural = 'stockproducts'

    def __str__(self):
        return self.product.name

    def save(self, *args, **kwargs):
        self.category = self.product.category
        # if self.image:
        #    self.image = get_thumbnail(self.image, '570x320').url
        super(StockProduct, self).save(*args, **kwargs)

