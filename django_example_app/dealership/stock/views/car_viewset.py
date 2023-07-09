from rest_framework import viewsets

from stock.models import Car
from stock.serialisers import CarSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
