import random
from Entities.items import Potion, Weapon, Armor

class LootTable:
    def __init__(self):
        self.enemy_drops = {
            "Witch": [
                ("Gold", 40, 1.0),  # (item_name, amount, drop_chance)
                (Weapon("Magic Wand 🪄", None, 10), 1, 0.2),
                (Potion("Health Potion 🧪", 30), 1, 0.5),
            ],
            "Skeleton": [
                ("Gold", 25, 1.0),
                (Weapon("Bone Bow 🦴🏹", None, 8), 1, 0.3),
                (Armor("Dusty Leather Boots 👢", defense_bonus=2, slot="feet"), 1, 0.4)
            ],
            "Spider": [
                ("Gold", 25, 1.0),
                (Weapon("Spider Fang 🕷️", None, 10), 1, 0.5),         
            ],
            "Zombie": [
                ("Gold", 20, 1.0),
                (Weapon("Rotten Club 🪵", None, 6), 1, 0.25),
                (Armor("Tattered Chestplate 🛡️", defense_bonus=1, slot="chest"), 1, 0.2),
                (Potion("Health Potion 🧪", 20), 1, 0.2),
            ],
            "Enderman": [
                ("Gold", 60, 1.0),
                (Weapon("Void Blade ⚔️", None, 15), 1, 0.15),
                (Armor("Shadow Hood 🕶️", defense_bonus=3, slot="head"), 1, 0.2),
                (Potion("Health Potion 🧪", 40), 1, 0.35),
            ],
            "Stone Golem Guardian": [
                ("Gold", 80, 1.0),
                (Weapon("Cracked Stone Hammer 🔨", None, 16), 1, 0.25),
                (Armor("Runed Stone Plate 🪨", defense_bonus=4, slot="chest"), 1, 0.25),
                (Armor("Granite Greaves 🪨", defense_bonus=3, slot="legs"), 1, 0.2),
                (Potion("Health Potion 🧪", 50), 1, 0.35),
            ],
            "Ender Dragon": [
                ("Gold", 150, 1.0),
                (Weapon("Dragon Claw 💠", None, 22), 1, 0.35),
                (Armor("Dragon Scale Chestplate 🐉", defense_bonus=7, slot="chest"), 1, 0.25),
                (Potion("Enchanted Golden Apple ✨🍎", 100), 1, 0.35),
                (Potion("Golden Apple 🍎", 50), 2, 0.6),
            ]
        }

        self.world_drops = [
            ("Gold", 15, 0.8),
            (Potion("Health Potion 🧪", 30), 1, 0.3),
            (Potion("Cooked Steak 🥩", 10), 3, 0.5),
            (Weapon("Rusty Iron Sword ⚔️", None, 5), 1, 0.2),
            (Weapon("Shiny Iron Axe 🪓", None, 7), 1, 0.1),

            (Armor("Leather Helmet 🪖", defense_bonus=1, slot="head"), 1, 0.3),
            (Armor("Leather Chestplate 🛡️", defense_bonus=2, slot="chest"), 1, 0.3),
            (Armor("Leather Leggings 🦵", defense_bonus=2, slot="legs"), 1, 0.3),
            (Armor("Leather Boots 👢", defense_bonus=1, slot="boots"), 1, 0.3),

            (Armor("Iron Helmet 🪖", defense_bonus=2, slot="head"), 1, 0.08),
            (Armor("Iron Chestplate 🛡️", defense_bonus=3, slot="chest"), 1, 0.08),
            (Armor("Iron Leggings 🦵", defense_bonus=2, slot="legs"), 1, 0.08),
            (Armor("Iron Boots 👢", defense_bonus=2, slot="boots"), 1, 0.08),

            (Weapon("Diamond Sword 💎⚔️", None, 15), 1, 0.04),
            (Weapon("Diamond Axe 💎🪓", None, 14), 1, 0.03),
            (Armor("Diamond Helmet 💎🪖", defense_bonus=4, slot="head"), 1, 0.03),
            (Armor("Diamond Chestplate 💎🛡️", defense_bonus=6, slot="chest"), 1, 0.03),
            (Armor("Diamond Leggings 💎🦵", defense_bonus=5, slot="legs"), 1, 0.03),
            (Armor("Diamond Boots 💎👢", defense_bonus=4, slot="feet"), 1, 0.03),
            (Potion("Golden Apple 🍎", 50), 1, 0.10),
            (Potion("Enchanted Golden Apple ✨🍎", 100), 1, 0.02),            
        ]

    def get_enemy_loot(self, enemy_name):
        """Return loot drops from a defeated enemy."""
        if enemy_name not in self.enemy_drops:
            return []
        loot_obtained = []
        for item, amount, chance in self.enemy_drops[enemy_name]:
            if random.random() <= chance:
                loot_obtained.append((item, amount))
        return loot_obtained

    def get_world_loot(self):
        """Return random loot from world exploration."""
        loot_obtained = []
        for item, amount, chance in self.world_drops:
            if random.random() <= chance:
                loot_obtained.append((item, amount))
        return loot_obtained

    # ===== NEW METHOD =====
    def get_drops(self, enemy_name, area=None):
        """Alias for get_enemy_loot so battle.py works unchanged."""
        return self.get_enemy_loot(enemy_name)