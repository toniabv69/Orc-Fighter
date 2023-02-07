from entity import Entity
from random import randrange


class Hero(Entity):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id):
        super().__init__(name, health, level, mana, health_mult)
        self.AttackMult = 1
        self.DefaultAttackMult = self.AttackMult
        self.Nickname = nickname
        self.ClassId = class_id
        self.Moves = [["Attack", 1, 23, 27, 15, 0], ["Heal", 2, 21, 25, 10, 1], ["Focus", 3, 0.09, 0.11, 5, 2], [], ["Mana Restore", 5, 40, 45, 0, 3]]  # [name, id, min_stat, max_stat, mana_cost, move_type]
        self.DefaultCritChance = 0.1
        self.CritChance = self.DefaultCritChance
        self.CritMult = 2
        self.Experience = experience
        self.NeededExp = 20
        for i in range(2, level + 1, 1):
            self.NeededExp += (i * 10)

    def __str__(self):
        return f'{self.Name} the {self.Nickname}'

    def level_up(self):
        self.Level += 1
        self.MaxHealth = int(self.MaxHealth * 1.05)
        self.LevelAttackMult += (8 + self.Level) / 100
        self.Experience -= self.NeededExp
        self.NeededExp += self.Level * 10

    def focus(self, move_id):
        self.CritChance += (randrange(int(self.Moves[move_id][2] * 100), int(self.Moves[move_id][3] * 100), 1)) / 100

