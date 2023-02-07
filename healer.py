from hero import Hero


class Healer(Hero):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id):
        super().__init__(name, health, nickname, level, experience, mana, health_mult, class_id)
        self.Moves[0] = ["Attack", 1, 15, 18, 15, 0]
        self.Moves[1] = ["Heal", 2, 29, 32, 13, 1]
        self.Moves[3] = ["Ultimate Regen", 4, 40, 45, 30, 1]