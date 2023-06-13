from lesson_6_mvc_practice.car import Car, Money


class CarController:
    def get_cars(self):
        return [Car("1", "RED", "NISSAN", 2013, Money(1000000, "USD"))]
