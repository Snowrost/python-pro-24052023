class Teacher:
    def __init__(self):
        self.teacher_id = 1
        self._state = "EMPLOYED"

    def fire(self):
        self._state = "FIRED"

    def state(self):
        return self._state


def main():
    teacher = Teacher()
    teacher.fire()

    assert teacher.state() == "FIRED"

