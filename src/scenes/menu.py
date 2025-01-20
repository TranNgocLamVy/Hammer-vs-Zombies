import pygame
from typing import List

from src.utils.constants import *
from src.objects.hammer_cursor import Cursor
from src.objects.zombie import ZombieManager
from src.objects.game_manager import GameManager
from src.utils.scene import Scene, SceneManager
from src.ui.button import Button
from src.ui.pause_menu import PauseMenu
from src.ui.game_over import GameOver

class MenuScene(Scene):
  def __init__(self, name, screen: pygame.Surface, clock: pygame.time.Clock, scene_manager: SceneManager):
    super().__init__(name, screen, clock, scene_manager)

    self.background = pygame.image.load("assets/background/hvz_bg.png").convert_alpha()
    self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    self.brand = pygame.image.load("assets/sprites/brand.png").convert()
    self.brand.set_colorkey("white")
    self.brand = pygame.transform.scale(self.brand, (self.brand.get_width(), self.brand.get_height()))

    play_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, "Play game", 40, (0, 205, 0) ,on_click=lambda: scene_manager.change_scene("game"), padding_x=40, padding_y=20)

    quit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75, 0, "Quit game", 40, (0, 205, 0) ,on_click=lambda: pygame.quit(), padding_x=40, padding_y=20)

    self.add_ui(play_button)
    self.add_ui(quit_button)


  def handle_events(self, events: List[pygame.event.Event]):

    if pygame.mixer.music.get_busy() == False:
      pygame.mixer.music.load("assets/music/Intro.mp3")
      pygame.mixer.music.play(1, 0.0)

    for ui in self.uis:
      ui.handle_events(events)

    for obj in self.objects:
      obj.handle_events(events)

  def draw(self):
    self.screen.blit(self.background, (0, 0))
    self.screen.blit(self.brand, (SCREEN_WIDTH // 2 - self.brand.get_width() // 2, 150))

    for obj in self.objects:
      obj.draw(self.screen)

    for ui in self.uis:
      ui.draw(self.screen)

  def init_scene(self):
    pygame.mouse.set_visible(True)
    pygame.mixer.music.load("assets/music/Intro.mp3")
    pygame.mixer.music.play(1, 0.0)