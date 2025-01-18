import pygame
from typing import List
from src.utils.scene import Scene

class HomeScene(Scene):
  def __init__(self, name, screen: pygame.Surface, clock: pygame.time.Clock):
    super().__init__(name, screen, clock)
    self.add_object(self.cursor)
    

  def draw(self):
    pass
  
  def handle_events(self, envets: List[pygame.event.Event]):
    pass