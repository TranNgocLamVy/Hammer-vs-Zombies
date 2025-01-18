from enum import Enum

# Window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Hammer Cursor
HAMMER_CURSOR_ANGLE_START = 0
HAMMER_CURSOR_ANGLE_END = 120
HAMMER_CURSOR_ROTATION_SPEED = 40

# GameObjects
class GameObjectState(Enum):
  NOT_VISIBLE = 0
  VISIBLE = 1
  DESTROYED = 2

# Player
PLAYER_MAX_HP = 10

# Zombie
ZOMBIE_MIN_LIFETIME = 2000
ZOMBIE_MAX_LIFETIME = 3000
ZOMBIE_SPAWN_INTERVAL = 500
ZOMBIE_SPAWN_QUANTITY = 1
