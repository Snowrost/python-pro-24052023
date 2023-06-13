class Money:
    def __init__(self, amount: int, currency: str):
        self.amount = amount
        self.currency = currency


class Car:
    def __init__(self, car_id: str, color: str, make: str, year_of_production: int, price: Money):
        self.car_id = car_id
        self.color = color
        self.make = make
        self.year_of_production = year_of_production
        self.price = price

    def price(self, amount: Money):
        self.price = amount
        return self
