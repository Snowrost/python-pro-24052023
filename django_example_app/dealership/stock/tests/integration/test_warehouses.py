from django.test import TestCase
from django.urls import reverse
from stock.models import Warehouse


class WarehousesTest(TestCase):

    def test_get_warehouses(self):
        # given
        warehouse = Warehouse(name="test")
        warehouse.save()
        url = reverse("warehouses")

        # when
        response = self.client.get(url).json()

        # then
        self.assertEquals(response, {"warehouses": [{"id": str(warehouse.id), "name": warehouse.name}]})
