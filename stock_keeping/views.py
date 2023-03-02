from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED, HTTP_405_METHOD_NOT_ALLOWED

from .models import StockReading
from .serializers import StockReadingSerializer


class StockReadingList(ListCreateAPIView):
    serializer_class = StockReadingSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = StockReading.objects.filter(shop=self.request.user.profile.shop)\
            .order_by('GTIN', '-scanned_at').distinct('GTIN')
        if self.request.query_params.get('scanned_at__gt'):
            queryset = queryset.filter(scanned_at__gt=self.request.query_params.get('scanned_at__gt'))
        return queryset


class StockReadingBatchCreate(StockReadingList):
    def post(self, request, *args, **kwargs):
        serializer = StockReadingSerializer(data=request.data, many=True, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response(status=HTTP_201_CREATED)

    # to not harm auto-discovery and not confuse user

    def get(self, request, *args, **kwargs):
        return Response(status=HTTP_405_METHOD_NOT_ALLOWED)
    @property
    def allowed_methods(self):
        return ['POST', 'OPTIONS']
