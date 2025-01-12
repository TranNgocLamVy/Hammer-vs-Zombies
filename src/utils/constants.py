from enum import Enum

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# GameObjects
class GameObjectState(Enum):
  NOT_VISIBLE = 0
  VISIBLE = 1
  DESTROYED = 2
