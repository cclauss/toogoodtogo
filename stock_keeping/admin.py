from django.contrib import admin
from stock_keeping.models import StockReading,  Shop


admin.site.register(StockReading)
admin.site.register(Shop)

