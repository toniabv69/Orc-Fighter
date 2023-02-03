from entity import Entity
from random import randrange


class Hero(Entity):
    def __init__(self, name, health, nickname, level, experience):
        super().__init__(name, health, level)
        self.Nickname = nickname
        self.Moves = [["Attack", 1, 23, 27], ["Heal", 2, 21, 25], ["Focus", 3, 0.19, 0.21], ["Rage", 4, 0.19, 0.21]]  # [name, id, min_damage, max_damage]
        self.DefaultCritChance = 0.1
        self.CritChance = self.DefaultCritChance
        self.DefaultCritMult = 2
        self.CritMult = self.DefaultCritMult
        self.Experience = experience
        self.NeededExp = 20
        for i in range(2, level + 1, 1):
            self.NeededExp += (i * 10)

    def __str__(self):
        return f'{self.Name} the {self.Nickname}'

    def level_up(self):
        self.Level += 1
        self.MaxHealth += int((10 + self.Level - 2) / 2)
        self.LevelAttackMult += (10 + self.Level - 2) / 100
        self.Experience -= self.NeededExp
        self.NeededExp += self.Level * 10

    def focus(self):
        self.CritChance += (randrange(self.Moves[2][2] * 100, self.Moves[2][3] * 100, 1)) / 100

    def rage(self):
        self.CritMult += (randrange(self.Moves[3][2] * 100, self.Moves[3][3] * 100, 1)) / 100

