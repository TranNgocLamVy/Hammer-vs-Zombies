import pygame
from typing import List

from src.utils.constants import *
from src.utils.scene import Scene, SceneManager
from src.ui.button import Button


class GameOverScene(Scene):
  def __init__(self, name, screen: pygame.Surface, clock: pygame.time.Clock, scene_manager: SceneManager):
    super().__init__(name, screen, clock, scene_manager)

    self.font = pygame.font.Font(None, 60)
    play_again_button = Button(SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 50, 0, 10, 10, "Play Again", 24, "black", "white", self.on_play_again_click)
    self.uis.append(play_again_button)

    self.lose_sound = pygame.mixer.Sound("assets/sfx/lose.mp3")
  
  def handle_events(self, events: List[pygame.event.Event]):
    for ui in self.uis:
      ui.handle_events(events)

  def draw(self):
    pygame.mouse.set_visible(True)
    self.screen.fill("white") 
    self.draw_text()
    
    for ui in self.uis:
      ui.draw(self.screen)

  def init_scene(self):
    self.lose_sound.play()

  def draw_text(self):
    text = self.font.render("Game Over", True, (0, 0, 0))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    self.screen.blit(text, text_rect)
  
  def on_play_again_click(self):
    self.scene_manager.change_scene("game")
