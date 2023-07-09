from rest_framework import viewsets

from stock.models import Warehouse
from stock.serialisers import WarehouseSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
