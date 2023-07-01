import json
import uuid

from django.http import JsonResponse, HttpRequest
from django.views import View

from stock.models import Car


class CarsView(View):

    def get(self, request: HttpRequest):
        cars = Car.objects.all()
        return JsonResponse({"cars": [{"id": str(car.id),
                                       "name": car.name,
                                       "updated_date": str(car.updated_date),
                                       "created_date": str(car.created_date),
                                       "warehouse_id": str(car.warehouse.id)} for car in cars]})

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        car = Car(name=body["name"], warehouse_id=uuid.UUID(body["warehouse_id"]))
        car.save()
        return JsonResponse({"id": str(car.id)})
