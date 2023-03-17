from hero import Hero


class Mage(Hero):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id, gold, items):
        super().__init__(name, health, nickname, level, experience, mana, health_mult, class_id, gold, items)
        self._CritChance = 0
        self._DefaultCritChance = 0
        self._Moves[0] = ["Attack", 1, 31, 33, 20, 0]
        self._Moves[1] = ["Heal", 2, 15, 18, 15, 1]
        self._Moves[2] = ["Ultimate Attack", 3, 40, 45, 40, 0]
        self._Moves[3] = ["Ultimate Regen", 4, 40, 45, 40, 1]
        self._Moves[4] = ["Mana Restore", 5, 60, 65, 0, 3]
