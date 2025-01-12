from utils.constants import *

class GameObject:
    def __init__(self, x=0, y=0, z=0, sprite=None):
        self.x = x
        self.y = y
        self.z = z
        self.sprite = sprite
        self.State: GameObjectState = GameObjectState.NOT_VISIBLE

    def draw(self, surface):
        if self.sprite and self.State == GameObjectState.VISIBLE:
            surface.blit(self.sprite, (self.x, self.y))