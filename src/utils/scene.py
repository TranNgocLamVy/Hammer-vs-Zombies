import pygame
from typing import List

from src.utils.game_object import GameObject
from src.utils.ui import UI

class SceneManager(object): pass
class Scene(object): pass

class Scene(object):
  def __init__(self, name, screen: pygame.Surface, clock: pygame.time.Clock, scene_manager: SceneManager):
    self.name = name
    self.screen = screen
    self.clock = clock
    self.objects: List[GameObject] = [] 
    self.uis: List[UI] = []
    self.scene_manager = scene_manager

  def add_object(self, obj: GameObject):
    index = 0
    while index < len(self.objects) and self.objects[index].z <= obj.z:
      index += 1
    self.objects.insert(index, obj)
  
  def remove_object(self, obj: GameObject):
    if obj in self.objects:
      self.objects.remove(obj)

  def add_ui(self, ui: UI):
    index = 0
    while index < len(self.uis) and self.uis[index].z <= ui.z:
      index += 1
    self.uis.insert(index, ui)
  
  def remove_ui(self, ui: UI):
    if ui in self.uis:
      self.uis.remove(ui)
  
  def init_scene(self):
    raise NotImplementedError

  def draw(self):
    raise NotImplementedError

  def handle_events(self, _: List[pygame.event.Event]):
    raise NotImplementedError

  
class SceneManager(object):
  def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock):
    self.screen = screen
    self.clock = clock
    self.scenes = {}
    self.current_scene = None

  def add_scene(self, scene: Scene):
    self.scenes[scene.name] = scene

  def remove_scene(self, scene: Scene):
    if scene in self.scenes:
      self.scenes.pop(scene.name)
  
  def change_scene(self, scene_name):
    if scene_name in self.scenes:
      self.current_scene = self.scenes[scene_name]
      self.current_scene.init_scene()
    else:
      raise ValueError(f"Scene with name {scene_name} not found")
  
  def handle_events(self, events: List[pygame.event.Event]):
    self.current_scene.handle_events(events)
  
  def draw(self):
    self.current_scene.draw()
    pygame.display.flip()