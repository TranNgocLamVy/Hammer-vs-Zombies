import pygame
from typing import List
from src.utils.constants import *
import math

class GameManager(object):
  def __init__(self, clock: pygame.time.Clock):
    self.score = 0
    self.missed = 0
    self.hp = PLAYER_MAX_HP

    self.hp_sprite = pygame.image.load("assets/sprites/hp2.png").convert_alpha()
    self.hp_sprite = pygame.transform.scale(self.hp_sprite, (60, 60))

    self.font = pygame.font.Font("assets/font/font.ttf", 40)

    self.score_sprite = pygame.image.load("assets/sprites/zombie.png").convert_alpha()
    self.score_sprite = pygame.transform.scale(self.score_sprite, (50, 50))

    self.clock = clock
    self.time_multiplier = 1
    self.delta_time = 0
    self.is_paused = False

    self.zombie2_spawn_rate = 0.2
    self.garg_spawn_rate = 0
    self.zombie_spawn_quantity = ZOMBIE_SPAWN_QUANTITY
    self.zombie_spawn_interval = ZOMBIE_SPAWN_INTERVAL

    self.hp_spawn_rate = 0.02
  
  def draw(self, surface: pygame.Surface):
    self.draw_hp(surface)
    self.draw_score(surface)

  def draw_score(self, surface: pygame.Surface):
    background = pygame.Surface((130, 60))
    background.set_alpha(128)
    background.fill((0, 0, 0))
    surface.blit(background, (SCREEN_WIDTH - 130, 5))

    surface.blit(self.score_sprite, (SCREEN_WIDTH - 125, 10))

    score_text = self.font.render(f"x{self.score}", True, (0, 205, 0))
    text_rect = score_text.get_rect(center=(SCREEN_WIDTH - (score_text.get_width() / 2) - 10, 37),)
    surface.blit(score_text, text_rect)

  def draw_hp(self, surface: pygame.Surface):
    hp_sprite_x = 210
    hp_sprite_y = 5
    for i in range(self.hp):
      surface.blit(self.hp_sprite, (hp_sprite_x  + (i * 60) + 20, hp_sprite_y))
    
    self.adjust_difficulty()
  
  def handle_events(self, events: List[pygame.event.Event]):
    self.delta_time = self.clock.get_time() * self.time_multiplier
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x >= 233 and mouse_x <= 924 and mouse_y >= 79 and mouse_y <= 569:
          self.missed += 1

  def adjust_difficulty(self):
    # if self.score >= 10 and self.score < 20:
    #   self.zombie_spawn_quantity = 1
    #   self.zombie_spawn_interval = 1000
    #   self.garg_spawn_rate = 0.05
    # elif self.score >= 20 and self.score < 30:
    #   self.zombie_spawn_quantity = 2
    #   self.zombie_spawn_interval = 1000
    #   self.zombie2_spawn_rate = 0.25
    #   self.garg_spawn_rate = 0.075
    # elif self.score >= 30 and self.score < 40:
    #   self.zombie_spawn_quantity = 2
    #   self.zombie_spawn_interval = 800
    #   self.garg_spawn_rate = 0.1
    # elif self.score >= 40 and self.score < 50:
    #   self.zombie_spawn_quantity = 2
    #   self.zombie_spawn_interval = 750
    #   self.zombie2_spawn_rate = 0.3
    #   self.hp_spawn_rate = 0.05
    # elif self.score >= 50 and self.score < 100:
    #   self.zombie_spawn_quantity = 3
    #   self.zombie_spawn_interval = 1500
    #   self.hp_spawn_rate = 0.075
    # elif self.score >= 100:
    #   self.zombie_spawn_quantity = 3
    #   self.zombie_spawn_interval = 950
    #   self.zombie2_spawn_rate = 0.4
    #   self.garg_spawn_rate = 0.15
      
    #easy
      
    if self.score >= 10 and self.score < 20:
      self.zombie_spawn_quantity = 1
      self.zombie_spawn_interval = 1000
    elif self.score >= 20 and self.score < 50:
      self.zombie_spawn_quantity = 2
      self.zombie_spawn_interval = 1250
      self.zombie2_spawn_rate = 0.25
    elif self.score >= 50 and self.score < 75:
      self.zombie_spawn_quantity = 2
      self.zombie_spawn_interval = 1200
      self.garg_spawn_rate = 0.05
    elif self.score >= 75 and self.score < 100:
      self.zombie_spawn_quantity = 2
      self.zombie_spawn_interval = 1100
      self.zombie2_spawn_rate = 0.3
      self.garg_spawn_rate = 0.075
      self.hp_spawn_rate = 0.05
    elif self.score >= 100 and self.score < 150:
      self.zombie_spawn_quantity = 3
      self.zombie_spawn_interval = 1500
      self.hp_spawn_rate = 0.075
    elif self.score >= 150 and self.score < 200:
      self.zombie_spawn_quantity = 3
      self.zombie_spawn_interval = 1250
      self.zombie2_spawn_rate = 0.4
      self.garg_spawn_rate = 0.1
    elif self.score > 200:
      self.zombie_spawn_quantity = 2
      self.zombie_spawn_interval = 1500
      self.zombie2_spawn_rate = 0.85
      self.garg_spawn_rate = 0.15

  def hit_zombie(self, score: int = 1):
    self.score += score
    self.missed -= 1

  def heal(self):
    self.hp = min(self.hp + 1, PLAYER_MAX_HP)

  def is_game_over(self):
    return self.hp <= 0

  def reset(self):
    self.score = 0
    self.missed = 0
    self.time_multiplier = 1
    self.hp = PLAYER_MAX_HP
    self.zombie2_spawn_rate = 0.2
    self.garg_spawn_rate = 0
    self.zombie_spawn_quantity = ZOMBIE_SPAWN_QUANTITY
    self.zombie_spawn_interval = ZOMBIE_SPAWN_INTERVAL
    self.hp_spawn_rate = 0.02
    self.is_paused = False

  def pause(self):
    self.time_multiplier = 0
    self.is_paused = True
    pygame.mixer.music.set_volume(0.3)

  def un_pause(self):
    self.time_multiplier = 1
    self.is_paused = False
    pygame.mixer.music.set_volume(1)