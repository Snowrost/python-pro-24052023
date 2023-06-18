class Person:

    def __init__(self, first_name, last_name=None):
        self._first_name = first_name
        self._last_name = last_name

    def rename(self, first_name: str, last_name: str):
        pass


def main():
    person = Person("Ivan")
    another_person = Person("Ivan", "Niekipielov")
