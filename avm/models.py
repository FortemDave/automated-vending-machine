from django.db import models

# Create your models here.

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField(default=0)
    item_quantity_available = models.IntegerField(default=10)
    item_selected = models.IntegerField(default=0)
    def __str__(self):
        return self.item_name
