import pygame
from typing import List
from random import choice

from src.utils.constants import *
from src.objects.hammer_cursor import Cursor
from src.objects.zombie import ZombieManager
from src.objects.game_manager import GameManager
from src.utils.scene import Scene, SceneManager
from src.ui.button import Button
from src.ui.pause_menu import PauseMenu
from src.ui.game_over import GameOver

class GameScene(Scene):
  def __init__(self, name, screen: pygame.Surface, clock: pygame.time.Clock, scene_manager: SceneManager):
    super().__init__(name, screen, clock, scene_manager)

    self.background = pygame.image.load("assets/background/hvz_bg.png").convert_alpha()

    self.game_manager = GameManager(clock)
    self.cursor = Cursor(game_manager=self.game_manager)
    self.pause_menu = PauseMenu(self.game_manager, self, scene_manager)
    self.game_over = GameOver(self.game_manager, self, scene_manager)
  
    zombie_manager = ZombieManager(game_manager=self.game_manager, clock=self.clock)
    self.zombie_manager = zombie_manager
    self.add_object(zombie_manager)

    pause_button = Button(60, 40, 0, "Pause", 26, (0, 205, 0) ,on_click=lambda: self.game_manager.pause(), padding_x=20, padding_y=10)
    self.add_ui(pause_button)

    self.music = ["assets/music/Loonboon.mp3", "assets/music/Braniac.mp3", "assets/music/Ultimate.mp3"]


  def handle_events(self, events: List[pygame.event.Event]):
    self.game_manager.handle_events(events)
    self.pause_menu.handle_events(events)
    self.cursor.handle_events(events)
    self.game_over.handle_events(events)
    
    if pygame.mixer.music.get_busy() == 0:
      music = choice(self.music)
      pygame.mixer.music.load(music)
      pygame.mixer.music.play(1, 0.0)

    if self.game_manager.is_game_over():
      pygame.mixer.music.stop()
      self.game_manager.time_multiplier = 0

    if self.game_manager.is_paused or self.game_manager.is_game_over():
      return

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
    self.pause_menu.draw(self.screen)
    self.game_over.draw(self.screen)
    self.cursor.draw(self.screen)

  def init_scene(self):
    pygame.mouse.set_visible(False)
    self.game_manager.reset()
    self.zombie_manager.reset()
    music = choice(self.music)
    pygame.mixer.music.load(music)
    pygame.mixer.music.play(1, 0.0)