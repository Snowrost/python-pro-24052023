from lesson_6_mvc_practice.car import Car


class CarRepository:

    def __init__(self):
        # Initialise DB connection
        pass

    def get(self, car_id: str):
        pass

    def save(self, car: Car):
        pass

    def find_by_color_and_make(self, color: str, make: str) -> list:
        pass
