from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
import datetime


class CurrentYear(models.Model):
    year = models.IntegerField(_('year'), )
