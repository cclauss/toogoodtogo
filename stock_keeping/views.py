from rest_framework.generics import ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView

from .models import StockReading
from .serializers import StockReadingSerializer


class StockReadingList(ListCreateAPIView):
    queryset = StockReading.objects.order_by('GTIN', '-occurrence').distinct('GTIN')
    serializer_class = StockReadingSerializer


class StockReadingBatchCreate(APIView):
    def post(self, request):
        serializer = StockReadingSerializer(data=request.data, many=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=HTTP_201_CREATED)
