import json

from lesson_6_mvc_practice.car import Car


class CarSerialiser:

    @classmethod
    def to_json(cls, car: Car) -> str:
        return json.dumps({
            "id": car.car_id,
            "color": car.color,
            "make": car.make,
            "year_of_production": car.year_of_production,
            "price": {
                "amount": car.price.amount,
                "currency": car.price.currency
            }
        })
