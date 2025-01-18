import pygame
from typing import List
from src.utils.ui import UI
from src.utils.constants import *

class GameManager(UI):
  def __init__(self, x=0, y=0, z=0):
    super().__init__(x, y, z)
    self.score = 0
    self.missed = 0
    self.hp = PLAYER_MAX_HP

    self.hp_sprite = pygame.image.load("assets/sprites/hp.png").convert()
    self.hp_sprite.set_colorkey("white")
    self.hp_sprite = pygame.transform.scale(self.hp_sprite, (40, 40))

    self.font = pygame.font.Font(None, 36)

    self.time_divider = 1
  
  def draw(self, surface: pygame.Surface):
    self.draw_score(surface)
    self.draw_hp(surface)
    self.draw_missed(surface)

  def draw_score(self, surface: pygame.Surface):
    score_bg_width = 150
    score_bg_height = 50
    score_bg_x = (SCREEN_WIDTH // 2) - (score_bg_width // 2)
    score_bg_y = 10
    pygame.draw.rect(surface, (255, 255, 255), (score_bg_x, score_bg_y, score_bg_width, score_bg_height)) 

    score_text = self.font.render(f"Score: {self.score}", True, (0, 0, 0))
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 35))
    surface.blit(score_text, text_rect)
  
  def draw_hp(self, surface: pygame.Surface):
    hp_sprite_x = SCREEN_WIDTH - 50
    hp_sprite_y = 10

    for i in range(self.hp):
      surface.blit(self.hp_sprite, (hp_sprite_x, hp_sprite_y + (i * 40) + 10))

  def draw_missed(self, surface: pygame.Surface):
    missed_bg_width = 150
    missed_bg_height = 50
    missed_bg_x = (SCREEN_WIDTH // 2) - (missed_bg_width // 2) - 170
    missed_bg_y = 10
    pygame.draw.rect(surface, (255, 255, 255), (missed_bg_x, missed_bg_y, missed_bg_width, missed_bg_height)) 

    missed_text = self.font.render(f"Missed: {self.missed}", True, (0, 0, 0))
    text_rect = missed_text.get_rect(center=(SCREEN_WIDTH // 2 - 170 , 35))
    surface.blit(missed_text, text_rect)
  
  def handle_events(self, events: List[pygame.event.Event]):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= 233 and mouse_x <= 924 and mouse_y >= 79 and mouse_y <= 569:
          self.missed += 1

  def add_score(self, score: int):
    self.score += score

  def remove_hp(self):
    self.hp -= 1

  def is_game_over(self):
    return self.hp <= 0

  def reset(self):
    self.score = 0
    self.missed = 0
    self.hp = PLAYER_MAX_HP

  def set_time_divider(self, time_divider: int):
    self.time_divider = time_divider