from hero import Hero
from random import randrange


class Tank(Hero):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id, gold, items):
        super().__init__(name, health, nickname, level, experience, mana, health_mult, class_id, gold, items)
        self._Moves[0] = ["Attack", 1, 19, 22, 15, 0]
        self._Moves[1] = ["Heal", 2, 22, 26, 16, 1]
        self._Moves[3] = ["Ultimate Rage", 4, 0.12, 0.14, 25, 4]

    def rage(self, id):
        self._AttackMult += ((randrange(int(self._Moves[id][2] * 100), int(self._Moves[id][3] * 100), 1)) / 100)
