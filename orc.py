from entity import Entity


class Orc(Entity):
    def __init__(self, name, health, berserk_factor, level, experience_reward, mana, health_mult, gold_reward):
        super().__init__(name, health, level, mana, health_mult)
        self._BerserkFactor = berserk_factor
        self._ExpReward = experience_reward
        self._GoldReward = gold_reward
        self._Moves = [["Attack", 1, 15, 18, 15, 0], ["Heal", 2, 10, 13, 10, 1], ["Mana Restore", 5, 40, 45, 0, 3]]
        if self._BerserkFactor < 1:
            self._BerserkFactor = 1
        if self._BerserkFactor > 2:
            self._BerserkFactor = 2

    def get_berserk_factor(self):
        return self._BerserkFactor

    def get_gold_reward(self):
        return self._GoldReward

    def get_exp_reward(self):
        return self._ExpReward
