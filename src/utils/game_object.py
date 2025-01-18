import pygame
from typing import List
from src.utils.constants import *

class GameObject:
  def __init__(self, x=0, y=0, z=0, sprite=None, state: GameObjectState = None):
    self.x = x
    self.y = y
    self.z = z
    self.sprite = sprite
    self.state: GameObjectState = state

  def draw(self, surface: pygame.Surface):
    raise NotImplementedError
  
  def handle_events(self, events: List[pygame.event.Event]):
    raise NotImplementedError