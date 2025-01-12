import pygame
from components.constants import *


pygame.init()
pygame.display.set_caption("Test game")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True


player = pygame.Rect((100, 100, 50, 50))

delta_time = 0.1

velocity = 100

while running:
  screen.fill("white")
  pygame.draw.rect(screen, "red", player)

  key = pygame.key.get_pressed()

  if key[pygame.K_LEFT]:
    player.x -= velocity * delta_time
  if key[pygame.K_RIGHT]:
    player.x += velocity * delta_time
  if key[pygame.K_UP]:
    player.y -= velocity * delta_time
  if key[pygame.K_DOWN]:
    player.y += velocity * delta_time

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  delta_time = clock.tick(60) / 1000
  delta_time = min(delta_time, 0.1)

  pygame.display.flip()


pygame.quit()