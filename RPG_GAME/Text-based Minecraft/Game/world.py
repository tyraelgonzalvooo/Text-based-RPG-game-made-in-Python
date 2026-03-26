# world.py
from UI.textbox import border_line
from UI.utils import red, green, yellow
from Game.village import magical_merchant
from Game.inventory import show_inventory
from Game.enemy_manager import get_random_enemy
from Game.battle import battle
from UI.portraits import show_enemy, show_puzzle_art
from UI.textbox import border_line

# ──────────────────────────────────────────────
# PATH SELECTION
# ──────────────────────────────────────────────

def choose_path1():
    border_line()
    print("Choose your path:")
    print("1. Venture into the Dark Forest 🌲")
    print("2. Explore the Ancient Ruins 🏰")
    while True:
        choice = input("> ")
        if choice == '1':
            return "Dark Forest"
        elif choice == '2':
            return "Ancient Ruins"
        else:
            print("Invalid choice. Please enter 1 or 2.")
        border_line()


def choose_path2():
    border_line()
    print("Choose your path:")
    print("1. ")
    print("2. ")
    while True:
        choice = input("> ")
        if choice == '1':
            return "Dark Forest"
        elif choice == '2':
            return "Ancient Ruins"
        else:
            print("Invalid choice. Please enter 1 or 2.")
        border_line()


# ──────────────────────────────────────────────
# ENEMY → PORTRAIT MAPPING
# ──────────────────────────────────────────────
# All enemies now use the centralized show_enemy function
ENEMY_ART = {
    "Witch": show_enemy,
    "Skeleton": show_enemy,
    "Spider": show_enemy,
    "Zombie": show_enemy,
    "Enderman": show_enemy,
    "Stone Golem Guardian": show_enemy
    # Add new enemies here, images auto-detected
}


# ──────────────────────────────────────────────
# EXPLORATION & ENCOUNTERS
# ──────────────────────────────────────────────

def explore_forest(player, state, loot_table):
    """Handles random encounters in the Dark Forest."""
    enemy = get_random_enemy("Dark Forest")
    # Wrap the show_enemy function with a lambda to match battle's art_func signature
    art_func = lambda: ENEMY_ART[enemy.name](enemy.name)
    result = battle(player, enemy, state, loot_table, art_func=art_func)

    # Biome Chest Reward — Dark Forest
    if result == "win":
        border_line()
        print(green("🌲 The forest quiets... a mossy chest emerges from the roots."))
        print("You brush aside ivy and open the chest...")
        chest_loot = loot_table.get_world_loot()
        if chest_loot:
            print(green("\n🎁 Forest Chest Rewards:"))
            for item, amount in chest_loot:
                if isinstance(item, str) and item.lower() == "gold":
                    state.gold += amount
                    print(f"Added {yellow(amount)} {yellow('gold')} to your inventory")
                else:
                    player.inventory.add_item(item)
                    print(f"Added {amount}x {item.name} to your inventory")
        else:
            print("The chest crumbles to mulch — nothing useful inside this time.")
        # Magical merchant appears before inventory prompt
        magical_merchant(state)
        # Offer inventory access after chest, before next story beats
        choice = input("\nOpen your inventory to manage/use items? (y/n): ").lower().strip()
        if choice == 'y':
            show_inventory(player, state)
        border_line()
    return result


def explore_ruins(player, state, loot_table):
    """Handles random encounters in the Ancient Ruins."""
    enemy = get_random_enemy("Ancient Ruins")
    art_func = lambda: ENEMY_ART[enemy.name](enemy.name)
    result = battle(player, enemy, state, loot_table, art_func=art_func)

    # Biome Chest Reward — Ancient Ruins
    if result == "win":
        border_line()
        print(green("🏺 Amid collapsed stones, a rune-locked coffer clicks open."))
        print("Dust billows as you lift the lid...")
        chest_loot = loot_table.get_world_loot()
        if chest_loot:
            print(green("\n🎁 Ruins Chest Rewards:"))
            for item, amount in chest_loot:
                if isinstance(item, str) and item.lower() == "gold":
                    state.gold += amount
                    print(f"Added {yellow(amount)} {yellow('gold')} to your inventory")
                else:
                    player.inventory.add_item(item)
                    print(f"Added {amount}x {item.name} to your inventory")
        else:
            print("The coffer contains only crumbled tablets and dust.")
        # Magical merchant appears before inventory prompt
        magical_merchant(state)
        # Offer inventory access after chest, before next story beats
        choice = input("\nOpen your inventory to manage/use items? (y/n): ").lower().strip()
        if choice == 'y':
            show_inventory(player, state)
        border_line()
    return result

def forest_trial(player, state, loot_table):
    """Act 3A: The Trial of Beasts — survive multiple forest encounters."""
    from UI.textbox import border_line
    from UI.utils import red, green
    from Game.enemy_manager import get_random_enemy
    from Game.battle import battle
    import time

    border_line()
    print(red("🌲 The Trial of Beasts 🌲"))
    print("The forest itself watches as your trial begins...\n")
    border_line()

    waves = 3
    victories = 0

    for i in range(1, waves + 1):
        print(f"\n🔥 Wave {i} of {waves} 🔥")
        time.sleep(1)

        # Spawn random enemy from the forest pool, show portrait like standard battles
        enemy = get_random_enemy("Dark Forest")
        art_func = lambda: ENEMY_ART[enemy.name](enemy.name)
        result = battle(player, enemy, state, loot_table, art_func=art_func)

        if result == "win":
            victories += 1
            print(green(f"\n✅ You have survived Wave {i}."))
        elif result == "fled":
            print(red("\nYou fled the trial — the forest rejects your cowardice."))
            state.flags["forest_trial_completed"] = False
            return "fled"
        else:
            print(red("\n💀 You were defeated. The forest claims another soul..."))
            state.flags["forest_trial_completed"] = False
            return "lose"

        time.sleep(1.5)

    # Trial completed successfully
    if victories == waves:
        print(green("\n🌿 You have conquered the Trial of Beasts!"))
        print("The forest spirit hums softly, blessing your courage...")
        state.flags["forest_trial_completed"] = True

        # Reward player
        reward_gold = 50
        state.gold += reward_gold
        print(f"You receive {reward_gold} gold as a token of nature’s respect.")
        print("A faint whisper follows you: 'You walk with the wilds now.'")
        border_line()
        return "success"


# Inside ruins_puzzle(player, state):

def ruins_puzzle(player, state):
    """Act 3 Puzzle: The Echo Chamber in the Ancient Ruins."""
    border_line()

    show_puzzle_art("ancient_door")  # 🖼 show the puzzle art here

    print("You stand before the sealed stone door covered in ancient symbols.")
    print("Each ring bears a glowing mark: a SUN, an EYE, and a CUBE.")
    print("The wall nearby whispers faint inscriptions:")
    print(" 'They saw before they created...'")
    print(" 'They shaped the world from light...'")
    print(" 'And from that, the world took form.'")
    border_line()

    symbols = ["Sun", "Eye", "Cube"]
    correct_order = ["Eye", "Sun", "Cube"]

    print("\nThe rings await your touch.")
    print("Enter the correct order of activation (comma-separated):")
    print(f"Symbols: {', '.join(symbols)}")
    player_choice = input("> ").split(",")
    player_choice = [s.strip().title() for s in player_choice]

    border_line()
    if player_choice == correct_order:
        show_puzzle_art("echo_chamber")  # Optional: reveal success image
        print("The rings align with a deep rumble.")
        print("Stone grinds against stone as the massive door begins to open...")
        print("Beyond it lies a golden chamber, humming with ancient energy.")
        print("You sense that something powerful — and forgotten — sleeps within.")
        state.flags["ruins_puzzle_solved"] = True
        return "success"
    else:
        show_puzzle_art("glowing_symbols")  # Optional: show failure glow effect
        print("The symbols flicker and fade...")
        print("A harsh grinding sound echoes through the ruins.")
        print("The air grows heavy — and something begins to move in the shadows.")
        state.flags["ruins_puzzle_solved"] = False
        return "failure"
