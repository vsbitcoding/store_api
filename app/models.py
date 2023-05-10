from django.db import models

# Create your models here.


class StoreCode(models.Model):
    code = models.CharField(max_length=1000, blank=True, null=True)
    name = models.CharField(max_length=1000, blank=True, null=True)
    old_location = models.CharField(max_length=1000, blank=True, null=True)
    new_location = models.CharField(max_length=1000, blank=True, null=True)
    coming_stock = models.CharField(max_length=1000, null=True, blank=True)
    stock = models.CharField(max_length=1000, null=True, blank=True)
    is_delete = models.BooleanField(default=False)
