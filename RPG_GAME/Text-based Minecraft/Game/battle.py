# battle.py
from Game.inventory import show_potions_menu
from UI.textbox import border_line
from UI.utils import red, green, yellow, cls
import random

# ===== ANSI COLORS =====
RESET = "\033[0m"
RED = "\033[91m"
GREEN = "\033[92m"
BOLD = "\033[1m"


def color_text(text, color):
    return f"{color}{text}{RESET}"


def display_health_bar(entity, current, maximum, is_player=True):
    """Draws a color-coded, dynamic health bar and shows stats below."""
    bar_length = 25
    ratio = current / maximum if maximum > 0 else 0
    filled_length = int(bar_length * ratio)
    empty_length = bar_length - filled_length

    color = GREEN if is_player else RED
    label_icon = "❤️" if is_player else "💀"
    filled = "█" * filled_length
    empty = "░" * empty_length
    bar = f"{color}{filled}{RESET}{empty}"

    colored_name = green(entity.name) if is_player else red(entity.name)

    print(f"{label_icon} {BOLD}{colored_name}’s HEALTH:{RESET} {current}/{maximum}")
    print(f"[{bar}]")

    if is_player:
        print(f"⚔️  Attack: {entity.attack_power_total}   🛡️  Defense: {entity.defense_total}\n")
    else:
        print(f"⚔️  Attack: {entity.attack_power}   🛡️  Defense: {entity.defense}\n")


def log_action(func):
    """Decorator to log whenever an action function runs."""
    def wrapper(*args, **kwargs):
        print(f"[Action] {func.__name__} executed.")
        return func(*args, **kwargs)
    return wrapper


# ===== Battle Function =====
@log_action
def battle(player, enemy, state, loot_table, art_func=None):
    """
    Handles turn-based combat between player and enemy.
    art_func: zero-argument callable that displays ASCII art of the enemy
    """
    border_line()
    print(f"\n⚔️  A wild {red(enemy.name)} appears!\n")

    player_max_hp = player.max_health
    enemy_max_hp = enemy.max_health
    turn = 1

    while player.is_alive() and enemy.is_alive():
        cls()
        border_line()

        # Show ASCII portrait if provided
        if art_func:
            art_func()

        print(red(enemy.name))
        print(f"🩸 Turn {turn}")
        border_line()

        display_health_bar(player, player._health, player_max_hp, is_player=True)
        display_health_bar(enemy, enemy._health, enemy_max_hp, is_player=False)

        # Player action choice
        print("❓ Choose an action")
        print("1. Attack")
        print("2. Heal")
        print("3. Flee")
        move = input("> ").lower().strip()

        if move == '1':
            player_attack(player, enemy)
        elif move == '2':
            show_potions_menu(player)
        elif move == '3':
            print(f"{green(player._name)} fled from battle! You live to fight another day...")
            return "fled"
        else:
            print("Invalid action.")
            continue

        # Enemy turn
        if enemy.is_alive():
            enemy_attack(enemy, player)

        input(red("\nPress Enter to continue..."))
        turn += 1

    # ===== Battle Outcome =====
    if player.is_alive():
        print(f"\n🎉 {red(enemy.name)} has been defeated!")

        # Get loot
        drops = loot_table.get_drops(enemy.name, area=getattr(enemy, "area", None))

        if drops:
            print(green("\n💰 Loot Obtained:"))
            for item, amount in drops:
                if isinstance(item, str) and item.lower() == "gold":
                    state.gold += amount
                    print(f"Added {yellow(amount)} {yellow('gold')} to your inventory")
                else:
                    player.inventory.add_item(item)
                    print(f"Added {amount}x {item.name} to your inventory")
        else:
            print("Nothing of value found this time.")

        return "win"
    else:
        print(red(f"\n💀 {green(player._name)} has fallen... Game Over."))
        return "lose"


# ===== Player & Enemy Attack Functions =====
def player_attack(player, enemy):
    """Player's attack action."""
    print("\n--- Player's Turn ---")
    player.attack(enemy)


def enemy_attack(enemy, player):
    """Enemy's attack action."""
    print("\n--- Enemy’s Turn ---")
    enemy.attack(player)