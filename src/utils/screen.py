import pygame
from utils.game_object import GameObject
from typing import List

class Screen(object):
  def __init__(self, name):
    self.name = name
    self.objects: List[GameObject] = [] 

  def add_object(self, obj: GameObject):
    index = 0
    while index < len(self.objects) and self.objects[index].z <= obj.z:
      index += 1
    self.objects.insert(index, obj)
