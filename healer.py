from hero import Hero


class Healer(Hero):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id, gold, items):
        super().__init__(name, health, nickname, level, experience, mana, health_mult, class_id, gold, items)
        self._Moves[0] = ["Attack", 1, 15, 18, 15, 0]
        self._Moves[1] = ["Heal", 2, 29, 32, 13, 1]
        self._Moves[3] = ["Ultimate Regen", 4, 40, 45, 30, 1]
