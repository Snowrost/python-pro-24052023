import json

from django.http import HttpRequest, JsonResponse
from django.views import View

from stock.models import Warehouse


class WarehouseView(View):
    def get(self, request):
        warehouses = Warehouse.objects.all()
        return JsonResponse(
            {
                "warehouses": [
                    {"id": str(warehouse.id), "name": warehouse.name}
                    for warehouse in warehouses
                ]
            }
        )

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        warehouse = Warehouse(name=body["name"])
        warehouse.save()
        return JsonResponse({"id": str(warehouse.id)})
