from Game.inventory import Inventory
import random

class Character:
    def __init__(self, name, health, attack_power):
        self._name = name
        self._max_health = health
        self._health = health
        self.attack_power = attack_power

    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @property
    def max_health(self):
        return self._max_health

    def is_alive(self):
        return self._health > 0

    def take_damage(self, amount):
        # Apply armor defense if available
        defense = getattr(self, "total_defense", 0)
        reduced_damage = max(amount - defense, 0)
        self._health -= reduced_damage
        if self._health < 0:
            self._health = 0

        if defense > 0:
            print(f"{self._name} blocked {defense} damage with armor!")
        print(f"{self._name} took {reduced_damage} damage! ({self._health}/{self._max_health})")

    def attack(self, other):
        """Handles standard attack with variance and critical chance."""
        variance = random.uniform(0.85, 1.15)
        base_damage = int(self.attack_power * variance)

        crit_chance = 0.05       # Default enemy crit rate
        crit_multiplier = 1.5

        if random.random() < crit_chance:
            base_damage = int(base_damage * crit_multiplier)
            print(f"💥 {self._name} lands a CRITICAL hit!")

        print(f"{self._name} attacks {other._name} for {base_damage} damage!")
        other.take_damage(base_damage)


class Player(Character):
    def __init__(self, name):
        super().__init__(name, 100, 15)
        self.inventory = Inventory()
        self.equipped_weapon = None
        self.equipped_armor = {
            "head": None,
            "chest": None,
            "legs": None,
            "feet": None
        }

    def heal(self, amount):
        self._health += amount
        if self._health > 100:  # Cap HP at 100
            self._health = 100
        print(f"{self._name} healed for {amount}! Current HP: {self._health}")

    @property
    def attack_power_total(self):
        """Include weapon bonus if equipped."""
        bonus = self.equipped_weapon.attack_bonus if self.equipped_weapon else 0
        return self.attack_power + bonus

    @property
    def defense_total(self):
        """Sum defense bonuses from all equipped armor."""
        total_defense = 0
        for armor_piece in self.equipped_armor.values():
            if armor_piece:
                total_defense += armor_piece.defense_bonus
        return total_defense


    def attack(self, other):
        """Player attack with slightly higher crit rate and weapon bonus."""
        variance = random.uniform(0.9, 1.1)
        base_damage = int(self.attack_power_total * variance)

        crit_chance = 0.15       # Player crit rate
        crit_multiplier = 1.75

        if random.random() < crit_chance:
            base_damage = int(base_damage * crit_multiplier)
            print(f"🔥 Critical hit! {self._name} deals {base_damage} damage!")

        print(f"{self._name} attacks {other._name} for {base_damage} damage!")
        other.take_damage(base_damage)


class Enemy(Character):
    def __init__(self, name, health, attack_power, defense=0):
        super().__init__(name, health, attack_power)
        self.defense = defense

    def take_damage(self, amount):
        reduced_damage = max(0, amount - self.defense)
        self._health -= reduced_damage
        if self._health < 0:
            self._health = 0

