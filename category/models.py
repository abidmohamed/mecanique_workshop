from django.db import models

# Create your models here.
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
from family.models import Family


class Category(models.Model):
    family = models.ForeignKey(Family, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250, null=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='categories/%Y/%m/%d', blank=True, )

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    # auto fill the slug when saving
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # if self.image:
        #    self.image = get_thumbnail(self.image, '570x320').url
        super(Category, self).save(*args, **kwargs)

    # def get_absolute_url(self):
        # TODO : Change it to the new url stock
        return reverse('stock:stockproductcategory_list', args=[self.id])
