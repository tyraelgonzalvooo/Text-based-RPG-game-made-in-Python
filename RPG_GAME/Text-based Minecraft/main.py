from Entities.characters import Player, Enemy
from Entities.items import Potion, Weapon
from Game.battle import battle
from Game.story import story1_generator, story2_generatorA, story2_generatorB, story3_generatorA, story3_generatorB
from Game.world import choose_path1, explore_forest, explore_ruins, ruins_puzzle, forest_trial, ENEMY_ART
from Game.village import village_hub
from Game.state import GameState
from Game.enemy_manager import get_random_enemy
from UI.splash import show_title, show_village, show_dark_forest, show_ancient_ruins
from UI.utils import safe_input, red, green, yellow, cls, type_out
from UI.textbox import border_line
from Game.inventory import show_inventory
from Game.loot import LootTable
import colorama

def main():
    colorama.init()
    cls()
    border_line()    
    show_title()
    border_line()

    # Character creator and setup
    name = safe_input("Enter your character's name: ")
    cls()
    player = Player(name)
    state = GameState(player)
    loot_table = LootTable()    

    # Start of adventure
    show_village()
    print(f"\nGreetings, {player._name}! Your adventure begins now.\n")
    for scene in story1_generator():
        type_out(f"📜 {scene}", color='yellow', skippable=True)
        safe_input(red("Press Enter to continue... \n"))
    
    # Give starting items
    player.inventory.add_item(Potion("Pumpkin Pie", 15))
    player.inventory.add_item(Weapon("Wooden Sword", 0, 5))
    print("Added 10 Gold 💰 to bag.")

    # Start
    village_hub(state)

    # Initial Inventory Setup
    print("Before your adventure begins, check your inventory...")
    show_inventory(player, state)    

    # Continue Main Loop
    path = choose_path1()
    print(f"You choose the {path} path.\n")

    # ───────────────────────────────
    # STORY BRANCHES
    # ───────────────────────────────

    if path == "Dark Forest":
        border_line()
        show_dark_forest()
        for scene in story2_generatorA():
            type_out(f"📜 {scene}", color='yellow', skippable=True)
            safe_input(red("Press Enter to continue... \n"))

        if state.flags.get("heard_about_witch", False):
            print("You recall the villagers’ warning about the witch.")
        border_line()
        explore_forest(player, state, loot_table)
        safe_input(red("Press Enter to continue... \n"))
        cls()

        # ACT 3A — Trial of Beasts
        for scene in story3_generatorA():
            type_out(f"📜 {scene}", color='yellow', skippable=True)
            safe_input(red("Press Enter to continue... \n"))
        forest_trial(player, state, loot_table)
        

    elif path == "Ancient Ruins":
        border_line()        
        show_ancient_ruins()
        for scene in story2_generatorB():
            type_out(f"📜 {scene}", color='yellow', skippable=True)
            safe_input(red("Press Enter to continue... \n"))
        border_line()
        explore_ruins(player, state, loot_table)
        safe_input(red("Press Enter to continue... \n"))
        cls()        

        # Act 3: The Puzzle of the Echo Chamber
        cls()
        for scene in story3_generatorB():
            type_out(f"📜 {scene}", color='yellow', skippable=True)
            safe_input(red("Press Enter to continue... \n"))

        result = ruins_puzzle(player, state)

        if result == "failure":
            print("\nA crumbling Stone Golem Guardian rises from the dust!")
            guardian = Enemy("Stone Golem Guardian", 120, 18, defense=4)
            art_func = lambda: ENEMY_ART[guardian.name](guardian.name)
            battle(player, guardian, state, loot_table, art_func=art_func)

    # ───────────────────────────────
    # FINAL ACT — The Ender Dragon
    # ───────────────────────────────
    border_line()
    type_out("A rift tears open in the sky, leaking violet light...", color='yellow', skippable=True)
    type_out("Eyes of End glow in your pack — a gate to The End beckons.", color='yellow', skippable=True)
    safe_input(red("Press Enter to step through... \n"))
    cls()
    border_line()
    type_out("You stand upon obsidian pillars under a starless void.", color='yellow', skippable=True)
    type_out("A shadow circles above — the Ender Dragon has awakened.", color='yellow', skippable=True)
    border_line()

    # Spawn the final boss
    final_boss = Enemy("Ender Dragon", 220, 25, defense=6)
    art_func = lambda: ENEMY_ART.get(final_boss.name, ENEMY_ART.get("Enderman"))(final_boss.name)
    result = battle(player, final_boss, state, loot_table, art_func=art_func)

    if result == "win":
        border_line()
        type_out("✧✧✧ V I C T O R Y ✧✧✧", color='yellow', skippable=True)
        type_out("🐉 The Ender Dragon spirals downward, its roar fading into the void...", color='yellow', skippable=True)
        type_out("Fragments of crystallized light gather around you, mending wounds and warming the air.", color='yellow', skippable=True)
        type_out("Villages will tell this tale — of courage, of hope, and of your name.", color='yellow', skippable=True)
        border_line()
        type_out("Legend whispers: the world is safe, for now.", color='green', skippable=False)
    elif result == "fled":
        border_line()
        type_out("You step back through the rift, the void wind tugging at your cloak...", color='yellow', skippable=True)
        type_out("The Dragon’s shadow still circles above The End. Another day, another chance.", color='yellow', skippable=True)

    border_line()
    type_out("✦ Thank you for playing this adventure ✦", color='yellow', skippable=False)
    type_out("Tip: Revisit the biomes, gear up, and face the Dragon again for new loot!", color='yellow', skippable=False)
    border_line()


if __name__ == "__main__":
    main()
