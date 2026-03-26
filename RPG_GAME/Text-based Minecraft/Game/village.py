from Entities.items import Potion, Weapon, Armor
from UI.textbox import border_line
from Game.loot import LootTable
from UI.utils import yellow, safe_input, cls



def village_hub(state):
    while True:
        border_line()
        print("🏘️  You are in the village. What would you like to do?\n")
        print("1. Explore around the village")
        print("2. Talk to the villagers")
        print("3. Visit the shop")
        print("4. Leave the village")

        choice = input("> ")

        if choice == "1":
            explore_village(state)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "2":
            talk_to_villagers(state)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "3":
            visit_shop(state)
            safe_input("\nPress Enter to continue...")
            cls()
        elif choice == "4":
            print("\n❗You leave the safety of the village and venture forth.")
            safe_input("\nPress Enter to continue...")
            cls()
            break
        else:
            print("\nInvalid choice. Try again.")
            safe_input("\nPress Enter to continue...")
            cls()
    border_line()   
        
def explore_village(state):
    # Check if the player already explored
    if getattr(state, "village_explored", False):
        print("\nYou've already explored the village. There's nothing new to find.")
        return

    # Mark as explored so it can't be repeated
    state.village_explored = True

    # Proceed with the loot event
    loot_system = LootTable()
    loot = loot_system.get_world_loot()
    if loot:
        print("\n✨ While exploring, you found:")
        for item, amount in loot:
            if isinstance(item, str) and item == "Gold":
                state.gold += amount
                print(f"Added {yellow(amount)} {yellow('gold')} to your inventory")
            else:
                state.inventory.add_item(item)
                # print(f" - {item.name}")
    else:
        print("You found nothing of value this time.")

def talk_to_villagers(state):
    if not state.flags["talked_to_villager"]:
        print("\n❗A villager warns you about a witch haunting the Dark Forest.")
        state.flags["talked_to_villager"] = True
        state.flags["heard_about_witch"] = True
    else:
        print("\n❗The villagers seem busy and have nothing new to say.")

def visit_shop(state):
    # Define shop catalog: (display_name, cost_gold, factory_callable)
    catalog = [
        ("Health Potion 🧪 (+30)", 5, lambda: Potion("Health Potion 🧪", 30)),
        ("Cooked Steak 🥩 (+10)", 3, lambda: Potion("Cooked Steak 🥩", 10)),
        ("Stone Sword ⚔️ (+6 ATK)", 12, lambda: Weapon("Stone Sword ⚔️", None, 6)),
        ("Iron Sword ⚔️ (+9 ATK)", 20, lambda: Weapon("Iron Sword ⚔️", None, 9)),
        ("Leather Helmet 🪖 (+1 DEF)", 10, lambda: Armor("Leather Helmet 🪖", defense_bonus=1, slot="head")),
        ("Leather Chestplate 🛡️ (+2 DEF)", 15, lambda: Armor("Leather Chestplate 🛡️", defense_bonus=2, slot="chest")),
        ("Leather Boots 👢 (+1 DEF)", 8, lambda: Armor("Leather Boots 👢", defense_bonus=1, slot="feet")),
    ]

    while True:
        border_line()
        print("🏪 The shopkeeper greets you warmly.")
        print(f"You have {yellow(state.gold)} {yellow('gold')} 💰.\n")
        print("What would you like to buy?")

        for idx, (label, cost, _) in enumerate(catalog, 1):
            print(f"{idx}. {label} — {cost} gold")
        print(f"{len(catalog) + 1}. Leave shop")

        choice = input("> ").strip()

        try:
            sel = int(choice)
        except ValueError:
            print("\n❗Invalid choice. Enter a number.")
            continue

        if sel == len(catalog) + 1:
            print("\n❗You leave the shop.")
            break

        if not (1 <= sel <= len(catalog)):
            print("\n❗Invalid choice. Try again.")
            continue

        label, cost, factory = catalog[sel - 1]
        if state.gold < cost:
            print("\n❗You don’t have enough gold.")
            continue

        item = factory()
        added = state.player.inventory.add_item(item)
        if added:
            state.gold -= cost
            print(f"\n❗Purchased {label} for {cost} gold.")
        else:
            print("\n❗Purchase failed — inventory full.")


def magical_merchant(state):
    """A traveling merchant appears briefly between stages with the same wares."""
    catalog = [
        ("Health Potion 🧪 (+30)", 5, lambda: Potion("Health Potion 🧪", 30)),
        ("Cooked Steak 🥩 (+10)", 3, lambda: Potion("Cooked Steak 🥩", 10)),
        ("Stone Sword ⚔️ (+6 ATK)", 12, lambda: Weapon("Stone Sword ⚔️", None, 6)),
        ("Iron Sword ⚔️ (+9 ATK)", 20, lambda: Weapon("Iron Sword ⚔️", None, 9)),
        ("Leather Helmet 🪖 (+1 DEF)", 10, lambda: Armor("Leather Helmet 🪖", defense_bonus=1, slot="head")),
        ("Leather Chestplate 🛡️ (+2 DEF)", 15, lambda: Armor("Leather Chestplate 🛡️", defense_bonus=2, slot="chest")),
        ("Leather Boots 👢 (+1 DEF)", 8, lambda: Armor("Leather Boots 👢", defense_bonus=1, slot="feet")),
    ]

    while True:
        border_line()
        print("🧙 The Magical Merchant emerges from a shimmer of light.")
        print(f"You have {yellow(state.gold)} {yellow('gold')} 💰.\n")
        for idx, (label, cost, _) in enumerate(catalog, 1):
            print(f"{idx}. {label} — {cost} gold")
        print(f"{len(catalog) + 1}. Leave")

        choice = input("> ").strip()
        try:
            sel = int(choice)
        except ValueError:
            print("\n❗Invalid choice. Enter a number.")
            continue

        if sel == len(catalog) + 1:
            print("\n✨ The merchant nods and fades away.")
            break

        if not (1 <= sel <= len(catalog)):
            print("\n❗Invalid choice. Try again.")
            continue

        label, cost, factory = catalog[sel - 1]
        if state.gold < cost:
            print("\n❗You don’t have enough gold.")
            continue

        item = factory()
        added = state.player.inventory.add_item(item)
        if added:
            state.gold -= cost
            print(f"\n❗Purchased {label} for {cost} gold.")
        else:
            print("\n❗Purchase failed — inventory full.")