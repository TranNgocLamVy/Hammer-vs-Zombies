import pygame
from typing import List

from src.utils.game_object import GameObject
from src.utils.constants import *
from src.objects.game_manager import GameManager

class Cursor(GameObject):
  def __init__(self, x=0, y=0, z=0, game_manager: GameManager=None):
    super().__init__(x, y, z)
    self.game_manager = game_manager
    self.state = GameObjectState.VISIBLE

    hammer = pygame.image.load("assets/sprites/hammer.png").convert_alpha()
    hammer = pygame.transform.scale(hammer, (hammer.get_width() / 2, hammer.get_height() / 2))
    self.hammer = pygame.transform.rotate(hammer, 0)

    crosshair = pygame.image.load("assets/sprites/crosshair.png").convert_alpha()
    crosshair = pygame.transform.scale(crosshair, (crosshair.get_width() / 2, crosshair.get_height() / 2))
    self.crosshair = crosshair

    self.sfx = pygame.mixer.Sound("assets/sfx/hammer.mp3")
    self.sfx.set_volume(0.2)

    self.is_animating = False
    self.rotation_angle = HAMMER_CURSOR_ANGLE_START
    self.rotation_speed = HAMMER_CURSOR_ROTATION_SPEED
    
  def draw(self, surface: pygame.Surface):
    if self.state != GameObjectState.VISIBLE:
      return
    
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if self.is_animating:
      self.rotation_angle += self.rotation_speed
      if self.rotation_angle >= HAMMER_CURSOR_ANGLE_END:
        self.rotation_speed = -self.rotation_speed
      if self.rotation_angle < HAMMER_CURSOR_ANGLE_START:
        self.rotation_speed = -self.rotation_speed
        self.rotation_angle = HAMMER_CURSOR_ANGLE_START
        self.is_animating = False
    rotated_sprite = pygame.transform.rotate(self.hammer, self.rotation_angle)
    rotated_rect = rotated_sprite.get_rect(center=(mouse_x + 35, mouse_y - 10))
    
    surface.blit(self.crosshair, (mouse_x - 15, mouse_y - 15))
    surface.blit(rotated_sprite, rotated_rect.topleft)

  def handle_events(self, events: List[pygame.event.Event]):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN and event.dict['button'] == 1:
        # print(pygame.mouse.get_pos())
        self.is_animating = True
        self.sfx.play()
