class Item:
    def __init__(self, name, effect):
        self.name = name
        self.effect = effect
    
class Potion(Item):
    def use(self, player):
        # Prevent wasting a potion at full HP
        if player.health >= player.max_health:
            print("⚠️ You're already at full health! No need to use a potion.")
            return False  # indicates potion was NOT used

        print(f"You used {self.name}!")
        player.heal(self.effect)
        return True  # indicates potion WAS used

class Weapon(Item):
    def __init__(self, name, effect, attack_bonus):
        super().__init__(name, effect)
        self.attack_bonus = attack_bonus

    def equip(self, player):
        player.equipped_weapon = self
        print(f"{player._name} equipped {self.name}! Attack increased by {self.attack_bonus}")
    
class Armor(Item):
    def __init__(self, name, defense_bonus, slot="body", description=""):
        super().__init__(name, description)
        self.defense_bonus = defense_bonus
        self.slot = slot  # e.g. "head", "body", "legs", "hands"

    def equip(self, player):
        """Equip this armor, replacing any existing armor in that slot."""
        current_armor = player.equipped_armor.get(self.slot)

        if current_armor == self:
            print(f"{self.name} is already equipped.")
            return

        if current_armor:
            print(f"Unequipped {current_armor.name}.")
            player.inventory.add_item(current_armor)

        player.equipped_armor[self.slot] = self
        player.inventory.remove_item(self.name)
        print(f"🛡️  Equipped {self.name}! (+{self.defense_bonus} defense)")