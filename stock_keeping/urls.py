from django.urls import path

from .views import StockReadingList, StockReadingBatchCreate

urlpatterns = [
    path('stock_reading/', StockReadingList.as_view()),
    path('stock_reading/batch/', StockReadingBatchCreate.as_view()),
]