from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    shop = models.OneToOneField('Shop', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.shop}"


class Shop(models.Model):
    name = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.name[:50]


class StockReading(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # longest GTIN seems to be 14
    # https://en.wikipedia.org/wiki/Global_Trade_Item_Number
    GTIN = models.CharField(max_length=14)
    expires_at = models.DateField()
    scanned_at = models.DateTimeField()

    def __str__(self):
        return f"{self.GTIN}: {self.expires_at} [{self.scanned_at}]"
