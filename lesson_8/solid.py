from typing import List


class Vehicle:

    def move(self):
        raise NotImplementedError("Interface cannot be run")

    def calculate_driver_salary(self):  # Wrong. You cannot break single responsibility principle
        pass


class Car(Vehicle):

    def __init__(self):
        self.make = "NISSAN"
        self.model = "NOTE"

    def move(self):
        print("move car for 100000 kilometers")


class LuxuryCar(Car):
    pass


class Lorry(Vehicle):
    pass


class Transportation:

    def __init__(self, vehicles: List[Vehicle]):
        self.vehicles = vehicles
        self.salary_calculator = SalaryCalculator()  # Wrong. Broken interface segregation principle.

    def transport(self):
        for vehicle in self.vehicles:
            vehicle.move()


class SalaryCalculator:
    pass
