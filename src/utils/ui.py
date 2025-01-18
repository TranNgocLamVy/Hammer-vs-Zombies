import pygame
from typing import List

class UI(object):
  def __init__(self, x: int = 0, y: int = 0, z: int = 0):
    self.x = x
    self.y = y
    self.z = z

  def draw(self, screen: pygame.Surface):
    raise NotImplementedError
  
  def handle_events(self, events: List[pygame.event.Event]):
    raise NotImplementedError
