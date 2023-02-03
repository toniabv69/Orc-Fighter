class Entity:
    def __init__(self, name, health, level):
        self.Name = name
        self.Health = health
        self.MaxHealth = self.Health
        self.Level = level
        self.LevelAttackMult = 1
        for i in range(2, level + 1, 1):
            self.LevelAttackMult += (10 + i - 2) / 100

    def is_alive(self):
        if self.Health == 0:
            return False
        else:
            return True

    def get_health(self):
        return self.Health

    def take_damage(self, damage_points):
        self.Health -= damage_points
        if self.Health < 0:
            self.Health = 0
        return 0

    def take_healing(self, healing_points):
        if not self.is_alive():
            return False
        self.Health += healing_points
        if self.Health > self.MaxHealth:
            self.Health = self.MaxHealth
        return True