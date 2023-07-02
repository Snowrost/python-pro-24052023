import json
import uuid

from django.http import HttpRequest, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from stock.models import Car, Warehouse


class CarsView(View):
    def get(self, request: HttpRequest):
        cars = Car.objects.all()
        json_response = {
            "cars": [
                {
                    "id": str(car.id),
                    "name": car.name,
                    "updated_date": str(car.updated_date),
                    "created_date": str(car.created_date),
                    "warehouse_id": str(car.warehouse.id),
                }
                for car in cars
            ]
        }
        if request.headers["accept"] == "application/json":
            return JsonResponse(json_response)
        else:
            context = {
                "cars": [
                    {
                        "name": car.name,
                        "updated_date": car.updated_date,
                        "created_date": car.created_date,
                        "warehouse_name": car.warehouse.name,
                    }
                    for car in cars
                ]
            }
            return render(request, "cars/cars_list.html", context, "text/html")

    def post(self, request: HttpRequest):
        body = json.loads(request.body)
        car = Car.objects.create(
            name=body["name"], warehouse_id=uuid.UUID(body["warehouse_id"])
        )
        return JsonResponse({"id": str(car.id)})


def create_car_view(request):
    if request.method == "GET":
        warehouses = Warehouse.objects.all()
        return render(request, "cars/create_car_form.html", {"warehouses": warehouses})
    elif request.method == "POST":
        Car.objects.create(
            name=request.POST["car_name"], warehouse_id=request.POST["warehouse_id"]
        )
        return HttpResponseRedirect(reverse("cars"))
