from hero import Hero


class Mage(Hero):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id):
        super().__init__(name, health, nickname, level, experience, mana, health_mult, class_id)
        self.CritChance = 0
        self.DefaultCritChance = 0
        self.Moves[0] = ["Attack", 1, 31, 33, 20, 0]
        self.Moves[1] = ["Heal", 2, 15, 18, 15, 1]
        self.Moves[2] = ["Ultimate Attack", 3, 40, 45, 40, 0]
        self.Moves[3] = ["Ultimate Regen", 4, 40, 45, 40, 1]
        self.Moves[4] = ["Mana Restore", 5, 60, 65, 0, 3]