import pygame
from typing import List
from random import random, choice, randint

from src.utils.constants import *
from src.utils.game_object import GameObject
from src.objects.game_manager import GameManager

class Zombie(GameObject):
  def __init__(self, x=0, y=0, z=0, index: int = 0, clock: pygame.time.Clock=None, game_manager: GameManager=None):
    super().__init__(x, y, z)
    self.clock = clock
    self.spot_index = index
    self.state = GameObjectState.VISIBLE
    self.game_manager = game_manager

    self.sfx1 = pygame.mixer.Sound("assets/sfx/zombie1.mp3")
    self.sfx1.set_volume(0.2)
    self.sfx2 = pygame.mixer.Sound("assets/sfx/zombie2.mp3")
    self.sfx2.set_volume(0.4)

    if random() > self.game_manager.zombie2_spawn_rate:
      self.image = pygame.image.load("assets/sprites/zombie.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (64, 64))
      self.hp = 1
    else:
      self.image = pygame.image.load("assets/sprites/zombie2.png").convert_alpha()
      self.image = pygame.transform.scale(self.image, (84, 84))
      self.hp = 2
      self.y -= 10

    self.rect = pygame.Rect(self.x, self.y, 64, 64)

    self.default_life_time = randint(ZOMBIE_MIN_LIFETIME, ZOMBIE_MAX_LIFETIME)
    self.life_time = self.default_life_time
  
  def handle_events(self, events: List[pygame.event.Event]):
    mouse_pos = pygame.mouse.get_pos()
    if not self.rect.collidepoint(mouse_pos) or self.state != GameObjectState.VISIBLE or self.game_manager.is_paused:
      return

    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
        self.hp -= 1
        if self.hp <= 0:
          self.state = GameObjectState.NOT_VISIBLE
          val = random()
          if val < 0.5:
            self.sfx1.play()
          elif val <= 1:
            self.sfx2.play()
        elif self.hp == 1:
          self.image = pygame.image.load("assets/sprites/zombie.png").convert_alpha()
          self.image = pygame.transform.scale(self.image, (64, 64))
          self.y += 10
        

  def draw(self, surface: pygame.Surface):
    self.rect.topleft = (self.x, self.y + (self.hp == 2) * 10)

    if self.state != GameObjectState.VISIBLE:
      return

    surface.blit(self.image, (self.x, self.y))

    self.life_time = max(self.life_time - self.game_manager.delta_time, 0)
    progress = self.life_time / self.default_life_time
    bar_width = 64
    bar_height = 5
    bar_x = self.x
    bar_y = self.y + 69 + (self.hp == 2) * 10
    if progress < 0.4:
      bar_color = (255, 0, 0)
    elif progress < 0.7:
      bar_color = (255, 255, 0)
    else:
      bar_color = (0, 255, 0)
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, bar_color, (bar_x, bar_y, bar_width * progress, bar_height))

class Brain(GameObject):
  def __init__(self, x=0, y=0, z=0, index: int = 0, clock: pygame.time.Clock=None, game_manager: GameManager=None):
    super().__init__(x, y, z)
    self.clock = clock
    self.spot_index = index
    self.state = GameObjectState.VISIBLE
    self.game_manager = game_manager

    self.image = pygame.image.load("assets/sprites/hp2.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (64, 64))
  
    self.rect = pygame.Rect(self.x, self.y, 80, 80)

    self.default_life_time = randint(ZOMBIE_MIN_LIFETIME, ZOMBIE_MAX_LIFETIME)
    self.life_time = self.default_life_time

  def handle_events(self, events: List[pygame.event.Event]):
    mouse_pos = pygame.mouse.get_pos()
    if not self.rect.collidepoint(mouse_pos) or self.state != GameObjectState.VISIBLE or self.game_manager.is_paused:
      return
    
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
        self.state = GameObjectState.NOT_VISIBLE

  def draw(self, surface: pygame.Surface):
    self.rect.topleft = (self.x, self.y)

    if self.state != GameObjectState.VISIBLE:
      return

    surface.blit(self.image, (self.x, self.y))

    self.life_time = max(self.life_time - self.game_manager.delta_time, 0)
    progress = self.life_time / self.default_life_time
    bar_width = 64
    bar_height = 5
    bar_x = self.x
    bar_y = self.y + 69
    if progress < 0.4:
      bar_color = (255, 0, 0)
    elif progress < 0.7:
      bar_color = (255, 255, 0)
    else:
      bar_color = (0, 255, 0)
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, bar_color, (bar_x, bar_y, bar_width * progress, bar_height))
  
class ZombieManager:
  def __init__(self, game_manager: GameManager, clock: pygame.time.Clock):
    self.zombies: List[Zombie] = []
    self.brains: List[Brain] = []
    self.spawn_timer = 0
    self.game_manager = game_manager
    self.clock = clock

    self.spawn_spots = [
      (238, 100), (310, 100), (388, 100), (460, 100), (538, 100), (610, 100), (688, 100), (760, 100), (838, 100),
      (238, 200), (310, 200), (388, 200), (460, 200), (538, 200), (610, 200), (688, 200), (760, 200), (838, 200),
      (238, 300), (310, 300), (388, 300), (460, 300), (538, 300), (610, 300), (688, 300), (760, 300), (838, 300),
      (238, 400), (310, 400), (388, 400), (460, 400), (538, 400), (610, 400), (688, 400), (760, 400), (838, 400),
      (238, 500), (310, 500), (388, 500), (460, 500), (538, 500), (610, 500), (688, 500), (760, 500), (838, 500),
    ]
    self.occupied_spots = [False] * len(self.spawn_spots)

  def draw(self, surface: pygame.Surface):

    self.spawn_timer += self.game_manager.delta_time

    if self.spawn_timer >= self.game_manager.zombie_spawn_interval:
      for _ in range(self.game_manager.zombie_spawn_quantity):
        self.spawn_zombie()
      self.spawn_timer = 0
      if random() < self.game_manager.hp_spawn_rate:
        self.spawn_brain()

    for zombie in self.zombies[:]:      
      if zombie.life_time <= 0:
        self.occupied_spots[zombie.spot_index] = False
        self.zombies.remove(zombie)
        self.game_manager.hp -= 1
      else:
        zombie.draw(surface)

    for brain in self.brains[:]:
      if brain.life_time <= 0:
        self.occupied_spots[brain.spot_index] = False
        self.brains.remove(brain)
      else:
        brain.draw(surface)

  def handle_events(self, events: List[pygame.event.Event]):
    for zombie in self.zombies[:]:
      zombie.handle_events(events)
      if zombie.state == GameObjectState.NOT_VISIBLE:
        self.occupied_spots[zombie.spot_index] = False
        self.zombies.remove(zombie)
        self.game_manager.hit_zombie()
    
    for brain in self.brains[:]:
      brain.handle_events(events)
      if brain.state == GameObjectState.NOT_VISIBLE:
        self.occupied_spots[brain.spot_index] = False
        self.brains.remove(brain)
        self.game_manager.heal()

  def spawn_zombie(self):
    available_spots = [i for i, occupied in enumerate(self.occupied_spots) if not occupied]
    if not available_spots:
      return

    spot_index = choice(available_spots)
    x, y = self.spawn_spots[spot_index]
    zombie = Zombie(x, y, 0, spot_index, self.clock, self.game_manager)
    self.zombies.append(zombie)
    self.occupied_spots[spot_index] = True

  def spawn_brain(self):
    available_spots = [i for i, occupied in enumerate(self.occupied_spots) if not occupied]
    if not available_spots:
      return

    spot_index = choice(available_spots)
    x, y = self.spawn_spots[spot_index]
    brain = Brain(x, y, 0, spot_index, self.clock, self.game_manager)
    self.brains.append(brain)
    self.occupied_spots[spot_index] = True
      

  def reset(self):
    self.zombies = []
    self.spawn_timer = 0
    self.occupied_spots = [False] * len(self.spawn_spots)