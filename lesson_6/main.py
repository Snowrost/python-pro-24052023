from lesson_6_mvc_practice.car_controller import CarController
from lesson_6_mvc_practice.car_serialiser import CarSerialiser


def main():
    cars = CarController().get_cars()
    print(CarSerialiser.to_json(cars[0]))


if __name__ == "__main__":
    main()
