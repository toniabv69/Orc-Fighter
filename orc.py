from entity import Entity


class Orc(Entity):
    def __init__(self, name, health, berserk_factor, level, experience_reward, mana, health_mult):
        super().__init__(name, health, level, mana, health_mult)
        self.BerserkFactor = berserk_factor
        self.ExpReward = experience_reward
        self.Moves = [["Attack", 1, 15, 18, 15, 0], ["Heal", 2, 10, 13, 10, 1], ["Mana Restore", 5, 40, 45, 0, 3]]
        if self.BerserkFactor < 1:
            self.BerserkFactor = 1
        if self.BerserkFactor > 2:
            self.BerserkFactor = 2



