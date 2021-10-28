from django.db import models
from django.db.models.fields import CharField

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=100)
    item_price = models.IntegerField(default=0)
    item_quantity_available = models.IntegerField(default=10)
    # item_selected = models.IntegerField(default=0)
    def __str__(self):
        return self.item_name

class order(models.Model):
    # order_id = models.AutoField(primary_key=True)
    phone_no = models.CharField(max_length=13, default="")
    items_json = models.CharField(max_length=2500, default="")