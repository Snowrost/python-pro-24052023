from django.urls import path

from .views.cars_view import CarsView, create_car_view
from .views.warehouses_view import WarehouseView

urlpatterns = [
    path(
        "warehouses/",
        WarehouseView.as_view(http_method_names=["get", "post"]),
        name="warehouses",
    ),
    path("cars/", CarsView.as_view(http_method_names=["get", "post"]), name="cars"),
    path("cars/create", create_car_view, name="create_car_form"),
]
