class GameState:
    def __init__(self, player):
        self.player = player
        self.location = "Village"
        self.gold = 10
        self.inventory = player.inventory
        self.flags = {
            "talked_to_villager": False,
            "heard_about_witch": False,
            "found_hidden_item": False,
        }
