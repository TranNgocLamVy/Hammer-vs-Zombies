import pygame
from typing import List

from src.objects.hammer_cursor import Cursor
from src.objects.zombie import ZombieManager
from src.objects.game_manager import GameManager
from src.utils.scene import Scene, SceneManager
from src.ui.button import Button

class GameScene(Scene):
  def __init__(self, name, screen: pygame.Surface, clock: pygame.time.Clock, scene_manager: SceneManager):
    super().__init__(name, screen, clock, scene_manager)

    self.background = pygame.image.load("assets/background/hvz_bg.png").convert_alpha()

    game_manager = GameManager()
    self.game_manager = game_manager
    self.cursor = Cursor(game_manager=game_manager)
  
    zombie_manager = ZombieManager(game_manager=game_manager, clock=self.clock)
    self.zombie_manager = zombie_manager
    self.add_object(zombie_manager)

  
  def handle_events(self, events: List[pygame.event.Event]):
    self.cursor.handle_events(events)
    self.game_manager.handle_events(events)
    
    for ui in self.uis:
      ui.handle_events(events)

    for obj in self.objects:
      obj.handle_events(events)

  def draw(self):
    self.screen.blit(self.background, (0, 0))

    for obj in self.objects:
      obj.draw(self.screen)

    for ui in self.uis:
      ui.draw(self.screen)

    self.game_manager.draw(self.screen)

    self.cursor.draw(self.screen)

    if self.game_manager.is_game_over():
      pygame.mixer.music.stop()
      self.scene_manager.change_scene("game_over")

  def init_scene(self):
    self.game_manager.reset()
    self.zombie_manager.reset()
    pygame.mixer.music.load("assets/music/main_theme.mp3")
    pygame.mixer.music.play(-1, 0.0)