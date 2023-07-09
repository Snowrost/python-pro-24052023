from rest_framework import serializers

from stock.models import Warehouse

from .dealer_serializer import DealerSerializer


class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name", "dealer"]

    def to_representation(self, instance):
        self.fields["dealer"] = DealerSerializer(read_only=True)
        return super(WarehouseSerializer, self).to_representation(instance)
