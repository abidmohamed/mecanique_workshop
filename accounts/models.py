from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext as _
# Create your models here.
import datetime


class CurrentYear(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    year = models.IntegerField(_('year'), )

    def __str__(self):
        return str(self.year) + " - " + str(self.user)
