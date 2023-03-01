from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from .models import StockReading
from .serializers import StockReadingSerializer


class StockReadingList(ListCreateAPIView):
    queryset = StockReading.objects.order_by('GTIN', '-scanned_at').distinct('GTIN')
    serializer_class = StockReadingSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]


class StockReadingBatchCreate(StockReadingList):
    def post(self, request, *args, **kwargs):
        serializer = StockReadingSerializer(data=request.data, many=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

    # to not harm auto-discovery and not confuse user
    @property
    def allowed_methods(self):
        return ['POST', 'OPTIONS', 'HEAD']
