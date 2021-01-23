from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Family(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.ImageField(upload_to='families/%Y/%m/%d', blank=True, )

    class Meta:
        ordering = ('name',)
        verbose_name = 'family'
        verbose_name_plural = 'families'

    def __str__(self):
        return self.name

    # auto fill the slug when saving
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        # if self.image:
        #    self.image = get_thumbnail(self.image, '570x320').url
        super(Family, self).save(*args, **kwargs)

    # provides a category_slug parameter to the
    # view for filtering products according to a given category.
    def get_absolute_url(self):
        return reverse('category:category_list', args=[self.id])
