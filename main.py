import pygame
import random
import time

random.seed(time.time())

from src.utils.constants import *
from src.utils.scene import SceneManager
from src.scenes.game import GameScene
from src.scenes.menu import MenuScene


pygame.init()
pygame.display.set_caption("Hammer vs Zombies")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

scene_manager = SceneManager(screen, clock)
menu = MenuScene("menu", screen, clock, scene_manager)
game = GameScene("game", screen, clock, scene_manager)

scene_manager.add_scene(menu)
scene_manager.add_scene(game)

scene_manager.change_scene("menu")

while running:
  events = pygame.event.get()

  for event in events:
    if event.type == pygame.QUIT:
      running = False

  scene_manager.handle_events(events)
  scene_manager.draw()

  clock.tick(60)
  pygame.display.flip()

pygame.quit()