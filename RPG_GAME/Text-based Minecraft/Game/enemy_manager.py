import random
from Entities.characters import Enemy

FOREST_ENEMIES = [
    {"name": "Witch", "hp": 60, "attack": 20},
    {"name": "Spider", "hp": 35, "attack": 5},
    {"name": "Zombie", "hp": 40, "attack": 10},
]

RUINS_ENEMIES = [
    {"name": "Skeleton", "hp": 35, "attack": 7},
    {"name": "Enderman", "hp": 70, "attack": 18},
]

# Dictionary linking area names to their enemy pools
ENEMY_POOLS = {
    "dark forest": FOREST_ENEMIES,
    "ancient ruins": RUINS_ENEMIES
}

def get_random_enemy(location: str):
    """
    Returns an Enemy instance from the specified location's pool.
    """
    pool = ENEMY_POOLS.get(location.lower())
    if not pool:
        raise ValueError(f"No enemy pool defined for location '{location}'")

    enemy_data = random.choice(pool)
    return Enemy(enemy_data["name"], enemy_data["hp"], enemy_data["attack"])