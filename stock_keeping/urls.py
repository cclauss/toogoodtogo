from django.urls import path

from .views import StockReadingList, StockReadingBatchCreate

urlpatterns = [
    path('stock_keeping/', StockReadingList.as_view()),
    path('stock_keeping/batch/', StockReadingBatchCreate.as_view()),
]