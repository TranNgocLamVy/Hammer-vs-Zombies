import pygame

from typing import List

from src.utils.constants import *
from src.utils.ui import UI
from src.objects.game_manager import GameManager
from src.ui.button import Button


class PauseMenu(UI):
  def __init__(self,game_manager: GameManager, game, scene_manager):
    super().__init__(0,0,100)
    self.game_manager = game_manager
    self.game = game
    self.scene_manager = scene_manager

    self.un_pause_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 0, "Resume game", 32,(0, 205, 0) ,on_click=lambda: self.game_manager.un_pause())
    self.reset_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 75, 0, "Reset game", 32,(0, 205, 0) ,on_click=lambda: self.game.init_scene())
    self.quit_button = Button(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150, 0, "Main menu", 32,(0, 205, 0) ,on_click=lambda: self.scene_manager.change_scene("menu"))

    background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.set_alpha(100)
    background.fill((0, 0, 0))
    self.background = background

    self.font = pygame.font.Font("assets/font/font.ttf", 60)
    

  def draw(self, surface: pygame.Surface):
    if not self.game_manager.is_paused:
      return
    
    surface.blit(self.background, (0, 0))
    
    
    text = self.font.render("Pause game", True, (0, 205, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    surface.blit(text, text_rect)

    self.un_pause_button.draw(surface)
    self.reset_button.draw(surface)
    self.quit_button.draw(surface)

  def handle_events(self, events: List[pygame.event.Event]):
    if not self.game_manager.is_paused:
      return

    self.un_pause_button.handle_events(events)
    self.reset_button.handle_events(events)
    self.quit_button.handle_events(events)
  