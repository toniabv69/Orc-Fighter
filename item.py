from random import randrange


class Item:
    def __init__(self, name, type, amplifier, amplifier_type, id, cost):
        self._Name = name
        self._Type = type
        self._Amplifier = amplifier
        self._AmplifierType = amplifier_type
        self._Id = id
        self._Cost = cost

    def __str__(self):
        return f"{self._Name} {self._Type}"

    def get_name(self):
        return self._Name

    def get_id(self):
        return self._Id

    def get_cost(self):
        return self._Cost

    def get_type(self):
        return self._Type

    def get_amplifier(self):
        return self._Amplifier

    def get_amplifier_type(self):
        return self._AmplifierType
