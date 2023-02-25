from django.db import models


class Shop(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)


class StockReading(models.Model):
    # shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # longest GTIN seems to be 14
    # https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    GTIN = models.CharField(max_length=14)
    expiry = models.DateField()
    occurrence = models.DateTimeField()

