from django.urls import path

from .views.warehouses_view import WarehouseView
from .views.cars_view import CarsView

urlpatterns = [
    path("warehouses/", WarehouseView.as_view(http_method_names=["get", "post"]), name="warehouses"),
    path("cars/", CarsView.as_view(http_method_names=["get", "post"]), name="cars"),
]
