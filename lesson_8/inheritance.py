class Person:

    def __init__(self):
        self._name = "Ivan"

    def rename(self, new_name):
        self._name = new_name

    def call_name(self):
        print(self._name)


class Teacher(Person):

    def __init__(self):
        super().__init__()
        self.teacher_id = 1
        self._state = "EMPLOYED"

    def fire(self):
        self._state = "FIRED"

    def state(self):
        return self._state

    def rename(self, new_name):
        super().rename("Miss " + new_name)


class Student(Person):
    pass


def main():
    teacher = Teacher()
    teacher.rename("Michael")


def call_names(person: Person):
    person.call_name()
