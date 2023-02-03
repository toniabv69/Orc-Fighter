from entity import Entity


class Orc(Entity):
    def __init__(self, name, health, berserk_factor, level, experience_reward):
        super().__init__(name, health, level)
        self.BerserkFactor = berserk_factor
        self.ExpReward = experience_reward
        self.Moves = [["Attack", 1, 15, 18], ["Heal", 2, 10, 13]]
        if self.BerserkFactor < 1:
            self.BerserkFactor = 1
        if self.BerserkFactor > 2:
            self.BerserkFactor = 2



