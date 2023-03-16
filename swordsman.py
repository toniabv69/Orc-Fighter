from hero import Hero


class Swordsman(Hero):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id, gold, items):
        super().__init__(name, health, nickname, level, experience, mana, health_mult, class_id, gold, items)
        self._CritMult = 2.25
        self._Moves[0] = ["Attack", 1, 31, 33, 18, 0]
        self._Moves[1] = ["Heal", 2, 15, 18, 10, 1]
        self._Moves[3] = ["Ultimate Slash", 4, 40, 45, 30, 0]
