from django.urls import include, path
from rest_framework import routers

from .views.car_viewset import CarViewSet
from .views.dealer_view import DealerView
from .views.warehouse_viewset import WarehouseViewSet

router = routers.DefaultRouter()
router.register(r"cars", CarViewSet)
router.register(r"warehouses", WarehouseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("dealers/", DealerView.as_view()),
    path("dealers/<uuid:pk>", DealerView.as_view())
]
