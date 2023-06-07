from entity import Entity
from random import randrange
from item import Item


class Hero(Entity):
    def __init__(self, name, health, nickname, level, experience, mana, health_mult, class_id, gold, items):
        super().__init__(name, health, level, mana, health_mult)
        self._AttackMult = 1
        self._DefaultAttackMult = self._AttackMult
        self._Nickname = nickname
        self._ClassId = class_id
        self._Moves = [["Attack", 1, 23, 27, 15, 0], ["Heal", 2, 21, 25, 10, 1], ["Focus", 3, 0.09, 0.11, 5, 2], [],
                       ["Mana Restore", 5, 40, 45, 0, 3]]  # [name, id, min_stat, max_stat, mana_cost, move_type]
        self._DefaultCritChance = 0.1
        self._CritChance = self._DefaultCritChance
        self._CritMult = 2
        self._Experience = experience
        self._NeededExp = 20
        self._Gold = gold
        if self._ClassId == 1:
            self._ClassItems = [Item("Basic", "Sword", 0.05, 0, 0, 50),
                                Item("Great", "Sword", 0.1, 0, 1, 200),
                                Item("Epic", "Sword", 0.3, 0, 2, 600),
                                Item("Legendary", "Sword", 0.6, 0, 3, 1200),
                                Item("Mythic", "Sword", 1, 0, 4, 2000),
                                Item("Godly", "Sword", 1.5, 0, 5, 4000),
                                Item("Focus", "Sash", 0.1, 4, 6, 500)]
            self._ClassItemTypes = ["Sword", "Sash"]
        elif self._ClassId == 2:
            self._ClassItems = [Item("Basic", "Healer Orb", 0.05, 1, 0, 50),
                                Item("Great", "Healer Orb", 0.1, 1, 1, 200),
                                Item("Epic", "Healer Orb", 0.3, 1, 2, 600),
                                Item("Legendary", "Healer Orb", 0.6, 1, 3, 1200),
                                Item("Mythic", "Healer Orb", 1, 1, 4, 2000),
                                Item("Godly", "Healer Orb", 1.5, 1, 5, 4000)]
            self._ClassItemTypes = ["Healer Orb"]
        elif self._ClassId == 3:
            self._ClassItems = [Item("Basic", "Armor", 0.05, 2, 0, 50),
                                Item("Great", "Armor", 0.1, 2, 1, 200),
                                Item("Epic", "Armor", 0.2, 2, 2, 600),
                                Item("Legendary", "Armor", 0.3, 2, 3, 1200),
                                Item("Mythic", "Armor", 0.5, 2, 4, 2000),
                                Item("Godly", "Armor", 0.7, 2, 5, 4000)]
            self._ClassItemTypes = ["Armor"]
        elif self._ClassId == 4:
            self._ClassItems = [Item("Basic", "Mana Restore Orb", 0.05, 3, 0, 50),
                                Item("Great", "Mana Restore Orb", 0.1, 3, 1, 200),
                                Item("Epic", "Mana Restore Orb", 0.3, 3, 2, 600),
                                Item("Legendary", "Mana Restore Orb", 0.6, 3, 3, 1200),
                                Item("Mythic", "Mana Restore Orb", 1, 3, 4, 2000),
                                Item("Godly", "Mana Restore Orb", 1.5, 3, 5, 4000),
                                Item("A-10", "Thunderbolt", 10, 0, 6, 99999)]
            self._ClassItemTypes = ["Mana Restore Orb", "Thunderbolt"]
        self._Items = []
        self._EquippedItems = []
        for item in items:
            if -1 < item < len(self._ClassItems):
                self.add_item(self._ClassItems[item])
                self.equip_item(item)
        for i in range(2, level + 1, 1):
            self._NeededExp += (i * 10)

    def __str__(self):
        return f'{self._Name} the {self._Nickname}'

    def level_up(self):
        self._Level += 1
        self._MaxHealth += int(self._Level * 1.5 * self._HealthMult)
        self._LevelAttackMult += (8 + self._Level) / 100
        self._Experience -= self._NeededExp
        self._NeededExp += self._Level * 10

    def add_item(self, item: Item):
        self._Items.append(item)

    def remove_item(self, item: Item):
        if item in self._Items:
            self._Items.remove(item)

    def get_equipped_items(self):
        return self._EquippedItems

    def get_class_item_types(self):
        return self._ClassItemTypes

    def equip_item(self, item_id):
        if self.is_type_equipped(self._ClassItems[item_id].get_type()):
            for item in self._EquippedItems:
                if item.get_type() == self._ClassItems[item_id].get_type():
                    self._EquippedItems.remove(item)
        self._EquippedItems.append(self._ClassItems[item_id])

    def unequip_item(self, item_id):
        for item in self._EquippedItems:
            if item.get_type() == self._ClassItems[item_id].get_type():
                self._EquippedItems.remove(item)

    def is_type_equipped(self, type):
        for item in self.get_equipped_items():
            if type == item.get_type():
                return True
        return False

    def get_class_items(self):
        return self._ClassItems

    def get_items(self):
        return self._Items

    def get_gold(self):
        return self._Gold

    def give_gold(self, amount):
        self._Gold += amount

    def spend_gold(self, amount):
        self._Gold -= amount
        if self._Gold < 0:
            self._Gold = 0

    def focus(self, move_id):
        extra = 0
        for item in self.get_equipped_items():
            if item.get_amplifier_type() == 4:
                extra += item.get_amplifier()
        self._CritChance += ((randrange(int(self._Moves[move_id][2] * 100),
                                       int(self._Moves[move_id][3] * 100), 1)) / 100) + extra

    def get_nickname(self):
        return self._Nickname

    def get_attack_mult(self):
        return self._AttackMult

    def get_default_attack_mult(self):
        return self._DefaultAttackMult

    def get_crit_chance(self):
        return self._CritChance

    def get_default_crit_chance(self):
        return self._DefaultCritChance

    def get_classid(self):
        return self._ClassId

    def get_crit_mult(self):
        return self._CritMult

    def set_crit_chance(self, crit_chance):
        self._CritChance = crit_chance

    def get_experience(self):
        return self._Experience

    def get_needed_exp(self):
        return self._NeededExp

    def give_experience(self, exp):
        self._Experience += exp
        level_check = 0
        while self._Experience >= self._NeededExp:
            self.level_up()
            level_check = 1
        if level_check == 1:
            return True
        else:
            return False
