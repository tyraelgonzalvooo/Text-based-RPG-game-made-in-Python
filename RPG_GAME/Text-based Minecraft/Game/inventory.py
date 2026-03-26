from Entities.items import Potion, Weapon, Armor
from Game import state
from UI.utils import safe_input, red, green, cls
from UI.textbox import border_line

class Inventory:
    def __init__(self, limit=20):
        self.items = []
        self.limit = limit

    def add_item(self, item):
        if len(self.items) >= self.limit:
            print("Your inventory is full!")
            return False
        self.items.append(item)
        print(f"Added {item.name} to inventory.")
        return True

    def remove_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                self.items.remove(item)
                print(f"Removed {item.name} from inventory.")
                return True
        print(f"No item named {item_name} found.")
        return False

    def list_items(self):
        if not self.items:
            print("Inventory is empty.")
            return
        print("Your Inventory:")
        for idx, item in enumerate(self.items, 1):
            if hasattr(item, "attack_bonus"):
                print(f"{idx}. {item.name} (Weapon, +{item.attack_bonus} Attack)")
            else:
                print(f"{idx}. {item.name} (Effect: {item.effect})")

    def get_item(self, item_name):
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return item
        return None
    
def show_inventory(player, state):
    """Inventory hub — manage weapons, armor, potions, and items."""
    while True:
        border_line()
        print(f"🎒  Inventory Menu — {player.name}")
        print(f"💰  Gold: {state.gold}\n")

        print("1. View All Items")
        print("2. Use Potion")
        print("3. Equip Weapon")
        print("4. Equip Armor")
        print("5. Drop Item")
        print("6. Back\n")

        choice = safe_input("> ").strip()

        if choice == "1":
            view_all_items(player)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "2":
            show_potions_menu(player)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "3":
            equip_weapon_menu(player)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "4":
            equip_armor_menu(player)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "5":
            drop_item_menu(player)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "6":
            safe_input("\nPress Enter to continue...")
            cls()
            break
        else:
            print("Invalid choice. Try again.")
            safe_input("\nPress Enter to continue...")
            cls()

def view_all_items(player):
    items = player.inventory.items
    if not items:
        print("\nYour inventory is empty.")
        return

    print("\n--- All Items ---\n")
    for idx, item in enumerate(items, 1):
        if isinstance(item, Weapon):
            print(f"{idx}. {item.name} (Weapon, +{item.attack_bonus} ATK)")
        elif isinstance(item, Armor):
            print(f"{idx}. {item.name} (Armor, +{item.defense_bonus} DEF, Slot: {item.slot})")
        elif isinstance(item, Potion):
            print(f"{idx}. {item.name} (Potion, Effect: {item.effect})")
        else:
            print(f"{idx}. {item.name}")

def show_potions_menu(player):
    potions = [item for item in player.inventory.items if isinstance(item, Potion)]
    if not potions:
        print("You have no potions to use!")
        return

    print("\n--- Potion Pouch ---")
    for idx, potion in enumerate(potions, 1):
        print(f"{idx}. {potion.name} (Effect: {potion.effect})")

    choice = safe_input("Choose a potion number or press Enter to cancel: ").strip()

    if choice == "":
        return

    try:
        index = int(choice) - 1
        if 0 <= index < len(potions):
            potion = potions[index]
            used = potion.use(player)
            # Only remove the potion if it was actually used
            if used:
                player.inventory.remove_item(potion.name)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")

def equip_weapon_menu(player):
    weapons = [i for i in player.inventory.items if isinstance(i, Weapon)]
    if not weapons:
        print("\nYou have no weapons to equip.")
        return

    print("\n--- Weapons ---")
    for idx, weapon in enumerate(weapons, 1):
        print(f"{idx}. {weapon.name} (+{weapon.attack_bonus} ATK)")

    choice = safe_input("Choose a weapon to equip or press Enter to cancel: ").strip()
    if not choice:
        return

    try:
        idx = int(choice) - 1
        weapon = weapons[idx]
        weapon.equip(player)
    except (ValueError, IndexError):
        print("Invalid selection.")

def equip_armor_menu(player):
    armors = [i for i in player.inventory.items if isinstance(i, Armor)]
    if not armors:
        print("\nYou have no armor pieces.")
        return

    print("\n--- Armor ---")
    for idx, armor in enumerate(armors, 1):
        print(f"{idx}. {armor.name} (+{armor.defense_bonus} DEF, Slot: {armor.slot})")

    choice = safe_input("Choose armor to equip or press Enter to cancel: ").strip()
    if not choice:
        return

    try:
        idx = int(choice) - 1
        armor = armors[idx]
        armor.equip(player)
    except (ValueError, IndexError):
        print("Invalid selection.")

def drop_item_menu(player):
    items = player.inventory.items
    if not items:
        print("\nYou have no items to drop.")
        return

    print("\n--- Drop Item ---")
    for idx, item in enumerate(items, 1):
        print(f"{idx}. {item.name}")

    choice = safe_input("Choose an item to drop or press Enter to cancel: ").strip()
    if not choice:
        return

    try:
        idx = int(choice) - 1
        item = items[idx]
        confirm = safe_input(f"Drop {item.name}? (y/n): ").lower().strip()
        if confirm == "y":
            player.inventory.remove_item(item.name)
            print(f"{red('Dropped')} {item.name}.")
    except (ValueError, IndexError):
        print("Invalid selection.")

def equip_armor(player):
    armors = [item for item in player.inventory.items if isinstance(item, Armor)]
    if not armors:
        print("You have no armor to equip!")
        return

    print("\n--- Armor Inventory ---")
    for i, armor in enumerate(armors, 1):
        print(f"{i}. {armor.name} (+{armor.defense_bonus} defense, slot: {armor.slot})")

    choice = input("Choose armor number or press Enter to cancel: ").strip()
    if choice == "":
        return

    try:
        index = int(choice) - 1
        if 0 <= index < len(armors):
            armor = armors[index]
            armor.equip(player)
        else:
            print("Invalid selection.")
    except ValueError:
        print("Please enter a number.")