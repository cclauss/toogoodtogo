from rest_framework import serializers

from stock_keeping.models import StockReading, Shop


class StockReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockReading
        fields = ['GTIN', 'expiry', 'occurrence']

    def create(self, validated_data):
        shop = self.context['request'].user.profile.shop
        validated_data['shop'] = shop
        return super().create(validated_data)
