import pygame

from typing import List

from src.utils.constants import *
from src.utils.ui import UI
from src.objects.game_manager import GameManager
from src.ui.button import Button


class GameOver(UI):
  def __init__(self,game_manager: GameManager, game, scene_manager):
    super().__init__(0,0,100)
    self.game_manager = game_manager
    self.game = game
    self.scene_manager = scene_manager

    self.play_again_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, "Play Again", 32,(0, 205, 0) ,on_click=lambda: self.play_again())
    self.quit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75, 0, "Main menu", 32,(0, 205, 0) ,on_click=lambda: self.to_menu())

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.set_alpha(100)
    background.fill((0, 0, 0))
    self.background = background

    self.is_init = True
    self.lose_sound = pygame.mixer.Sound("assets/sfx/lose.mp3")

    self.font = pygame.font.Font("assets/font/font.ttf", 60)

  def draw(self, surface: pygame.Surface):
    if not self.game_manager.is_game_over():
      return
    
    surface.blit(self.background, (0, 0))
    
    
    text = self.font.render("Game over", True, (0, 205, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    surface.blit(text, text_rect)

    self.play_again_button.draw(surface)
    self.quit_button.draw(surface)

  def to_menu(self):
    self.scene_manager.change_scene("menu")
    self.is_init = True

  def handle_events(self, events: List[pygame.event.Event]):
    if not self.game_manager.is_game_over():
      return
    
    if self.is_init:
      self.lose_sound.play()
      self.is_init = False

    self.play_again_button.handle_events(events)
    self.quit_button.handle_events(events)

  def play_again(self):
    self.game.init_scene()
    self.is_init = True

  