class Entity:
    def __init__(self, name, health, level, mana, health_mult):
        self._Name = name
        self._Health = health
        self._MaxHealth = self._Health
        self._Level = level
        self._LevelAttackMult = 1
        self._HealthMult = health_mult
        self._Mana = mana
        self._MaxMana = self._Mana
        self._Moves = []
        for i in range(2, level + 1, 1):
            self._LevelAttackMult += (8 + i) / 100

    def is_alive(self):
        if self._Health == 0:
            return False
        else:
            return True

    def get_name(self):
        return self._Name

    def get_health(self):
        return self._Health

    def get_max_health(self):
        return self._MaxHealth

    def get_level(self):
        return self._Level

    def get_mana(self):
        return self._Mana

    def get_health_mult(self):
        return self._HealthMult

    def get_max_mana(self):
        return self._MaxMana

    def take_damage(self, damage_points):
        self._Health -= damage_points
        if self._Health < 0:
            self._Health = 0
        return 0

    def take_healing(self, healing_points):
        if not self.is_alive():
            return False
        self._Health += healing_points
        if self._Health > self._MaxHealth:
            self._Health = self._MaxHealth
        return True

    def regen_mana(self, mana_points):
        if not self.is_alive():
            return False
        self._Mana += mana_points
        if self._Mana > self._MaxMana:
            self._Mana = self._MaxMana
        return True

    def spend_mana(self, mana_points):
        self._Mana -= mana_points
        return True

    def get_moves(self):
        return self._Moves

    def get_level_attack_mult(self):
        return self._LevelAttackMult

    def set_health(self, health):
        self._Health = health
        if self._Health < 0:
            self._Health = 0
        elif self._Health > self._MaxHealth:
            self._Health = self._MaxHealth

    def set_mana(self, mana):
        self._Mana = mana
        if self._Mana < 0:
            self._Mana = 0
        elif self._Mana > self._MaxMana:
            self._Mana = self._MaxMana
