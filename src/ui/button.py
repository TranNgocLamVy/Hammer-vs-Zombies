import pygame
from typing import List

from src.utils.constants import *
from src.utils.ui import UI

class Button(UI):
  def __init__(self, x=0, y=0, z=0, text="", font_size=24, font_color="black", on_click=None, padding_x=40, padding_y=20):
    super().__init__(x, y, z)
    self.text = text
    self.font_size = font_size
    self.font_color = font_color
    self.on_click = on_click

    self.font = pygame.font.Font("assets/font/font.ttf", self.font_size)
    self.text_surface = self.font.render(self.text, True, pygame.Color(self.font_color))
    self.text_width = self.text_surface.get_width()
    self.text_height = self.text_surface.get_height()

    self.button_left = pygame.image.load("assets/sprites/button_left.png").convert_alpha()
    self.button_middle = pygame.image.load("assets/sprites/button_middle.png").convert_alpha()
    self.button_right = pygame.image.load("assets/sprites/button_right.png").convert_alpha()

    self.padding_x = padding_x
    self.padding_y = padding_y
    self.width = self.text_width + 2 * self.padding_x
    self.height = max(self.text_height, self.button_middle.get_height()) + self.padding_y
    self.x = x - self.width // 2
    self.y = y - self.height // 2

    self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    self.button_middle = pygame.transform.scale(self.button_middle, (self.width - self.button_left.get_width() - self.button_right.get_width(), self.height))
    self.button_left = pygame.transform.scale(self.button_left, (self.button_left.get_width(), self.height))
    self.button_right = pygame.transform.scale(self.button_right, (self.button_right.get_width(), self.height))

  def draw(self, surface: pygame.Surface):
    surface.blit(self.button_left, (self.x, self.y))
    surface.blit(self.button_middle, (self.x + self.button_left.get_width(), self.y))
    surface.blit(self.button_right, (self.x + self.button_left.get_width() + self.button_middle.get_width(), self.y))
    text_x = self.x + (self.width - self.text_width) // 2
    text_y = self.y + (self.height - self.text_height) // 2 - 3
    surface.blit(self.text_surface, (text_x, text_y))

  def handle_events(self, events: List[pygame.event.Event]):
    for event in events:
      if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
          self.on_click()