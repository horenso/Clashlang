from ast import Num


class Runtime:
    def __init__(self):
        self.memory = dict()

    def __str__(self):
        s = str(self.memory)

    def assign_value(self, name: str, value: float):
        self.memory[name] = value

    def get_value(self, name: str) -> float:
        return self.memory.get(name, 0.0)
