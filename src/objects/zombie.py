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
    self.sfx1.set_volume(0.3)
    self.sfx2 = pygame.mixer.Sound("assets/sfx/zombie2.mp3")
    self.sfx2.set_volume(0.5)
    self.sfx_special = pygame.mixer.Sound("assets/sfx/zombie_special.mp3")
    self.sfx_special.set_volume(5)

    self.image = pygame.image.load("assets/sprites/zombie.png").convert_alpha()
    self.image = pygame.transform.scale(self.image, (64, 64))
    self.rect = pygame.Rect(self.x, self.y, 64, 64)

    self.default_life_time = randint(ZOMBIE_MIN_LIFETIME, ZOMBIE_MAX_LIFETIME)
    self.life_time = self.default_life_time
  
  def handle_events(self, events: List[pygame.event.Event]):
    mouse_pos = pygame.mouse.get_pos()
    if not self.rect.collidepoint(mouse_pos) or self.state != GameObjectState.VISIBLE:
      return

    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
        self.state = GameObjectState.NOT_VISIBLE
        val = random()
        if val < 0.7:
          self.sfx1.play()
        elif val < 0.95:
          self.sfx2.play()
        else:
          self.sfx_special.play()
        

  def draw(self, surface: pygame.Surface):
    self.rect.topleft = (self.x, self.y)

    if self.state != GameObjectState.VISIBLE:
      return

    surface.blit(self.image, (self.x, self.y))

    delta_time = self.clock.get_time() / self.game_manager.time_divider
    self.life_time -= max(delta_time, 0)
    progress = self.life_time / self.default_life_time
    bar_width = 64
    bar_height = 5
    bar_x = self.x
    bar_y = self.y + 64 + 5
    pygame.draw.rect(surface, (50, 50, 50), (bar_x, bar_y, bar_width, bar_height))
    pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * progress, bar_height))
  
class ZombieManager:
  def __init__(self, game_manager: GameManager, clock: pygame.time.Clock):
    self.zombies: List[Zombie] = []
    self.spawn_timer = 0
    self.game_manager = game_manager
    self.clock = clock
    self.spawn_quantity = ZOMBIE_SPAWN_QUANTITY
    self.spawn_interval = ZOMBIE_SPAWN_INTERVAL

    self.spawn_spots = [
      (238, 100), (310, 100), (388, 100), (460, 100), (538, 100), (610, 100), (688, 100), (760, 100), (838, 100),
      (238, 200), (310, 200), (388, 200), (460, 200), (538, 200), (610, 200), (688, 200), (760, 200), (838, 200),
      (238, 300), (310, 300), (388, 300), (460, 300), (538, 300), (610, 300), (688, 300), (760, 300), (838, 300),
      (238, 400), (310, 400), (388, 400), (460, 400), (538, 400), (610, 400), (688, 400), (760, 400), (838, 400),
      (238, 500), (310, 500), (388, 500), (460, 500), (538, 500), (610, 500), (688, 500), (760, 500), (838, 500),
    ]
    self.occupied_spots = [False] * len(self.spawn_spots)

  def draw(self, surface: pygame.Surface):
    delta_time = self.clock.get_time() / self.game_manager.time_divider

    self.spawn_timer += delta_time

    if self.spawn_timer >= self.spawn_interval:
      for _ in range(self.spawn_quantity):
        self.spawn_zombie()
      self.spawn_timer = 0

    for zombie in self.zombies[:]:      
      if zombie.life_time <= 0:
        self.occupied_spots[zombie.spot_index] = False
        self.zombies.remove(zombie)
        self.game_manager.remove_hp()
      else:
        zombie.draw(surface)


  def handle_events(self, events: List[pygame.event.Event]):
    for zombie in self.zombies[:]:
      zombie.handle_events(events)
      if zombie.state == GameObjectState.NOT_VISIBLE:
        self.occupied_spots[zombie.spot_index] = False
        self.zombies.remove(zombie)
        self.game_manager.add_score(1)
        self.game_manager.missed -= 1

    self.adjust_difficulty()

  def spawn_zombie(self):
    available_spots = [i for i, occupied in enumerate(self.occupied_spots) if not occupied]
    if not available_spots:
      return

    spot_index = choice(available_spots)
    x, y = self.spawn_spots[spot_index]
    zombie = Zombie(x, y, 0, spot_index, self.clock, self.game_manager)
    self.zombies.append(zombie)
    self.occupied_spots[spot_index] = True

  def adjust_difficulty(self):
    if self.game_manager.score >= 50:
      self.spawn_quantity = 2
      self.spawn_interval = 800
    elif self.game_manager.score >= 100:
      self.spawn_quantity = 2
      self.spawn_interval = 600
    elif self.game_manager.score >= 150:
      self.spawn_quantity = 3
      self.spawn_interval = 800
    elif self.game_manager.score >= 200:
      self.spawn_quantity = 3
      self.spawn_interval = 400
      

  def reset(self):
    self.zombies = []
    self.spawn_timer = 0
    self.spawn_quantity = ZOMBIE_SPAWN_QUANTITY
    self.spawn_interval = ZOMBIE_SPAWN_INTERVAL
    self.occupied_spots = [False] * len(self.spawn_spots)