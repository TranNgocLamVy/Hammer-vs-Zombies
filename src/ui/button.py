import pygame
from typing import List

from src.utils.constants import *
from src.utils.ui import UI

class Button(UI):
  def __init__(self, x=0, y=0, z=0, padx=10, pady=10, text="Button", font_size=24, font_color="black", bg_color="white", on_click=None):
    super().__init__(x, y, z)
    self.text = text
    self.font_size = font_size
    self.font_color = font_color
    self.bg_color = bg_color
    self.on_click = on_click

    self.font = pygame.font.Font(None, self.font_size)
    self.text_surface = self.font.render(self.text, True, pygame.Color(self.font_color))
    self.width = self.text_surface.get_width() + padx
    self.height = self.text_surface.get_height() + pady
    self.bg_surface = pygame.Surface((self.width, self.height))
    self.bg_surface.fill(pygame.Color(self.bg_color))
    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

  def draw(self, surface: pygame.Surface):
    surface.blit(self.bg_surface, (self.x, self.y))
    surface.blit(self.text_surface, (self.x + (self.width - self.text_surface.get_width()) // 2, self.y + (self.height - self.text_surface.get_height()) // 2))

  def handle_events(self, events: List[pygame.event.Event]):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
          self.on_click()