import pygame

# Base class for game objects
class GameObject:
    def __init__(self, x, y, z, image=None):
        self.x = x
        self.y = y
        self.z = z
        self.image = image  # Optional: Pygame surface for rendering
        self.visible = True

    def update(self, dt):
        """Update logic for the object."""
        pass

    def draw(self, surface):
        """Draw the object to the screen."""
        if self.image and self.visible:
            surface.blit(self.image, (self.x, self.y))


# Class representing a screen in the game
class Screen:
    def __init__(self, name):
        self.name = name
        self.objects = []  # List of GameObject instances

    def add_object(self, obj):
        """Add a game object to the screen."""
        self.objects.append(obj)

    def update(self, dt):
        """Update all objects in the screen."""
        for obj in self.objects:
            obj.update(dt)

    def draw(self, surface):
        """Draw all objects in the screen."""
        for obj in sorted(self.objects, key=lambda o: o.z):  # Sort by z-index
            obj.draw(surface)


# Class to manage different screens
class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.current_screen = None

    def add_screen(self, screen):
        """Add a screen to the manager."""
        self.screens[screen.name] = screen

    def switch_to(self, screen_name):
        """Switch to a different screen."""
        if screen_name in self.screens:
            self.current_screen = self.screens[screen_name]

    def update(self, dt):
        """Update the current screen."""
        if self.current_screen:
            self.current_screen.update(dt)

    def draw(self, surface):
        """Draw the current screen."""
        if self.current_screen:
            self.current_screen.draw(surface)


# Example usage
def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()

    # Create screen manager
    manager = ScreenManager()

    # Create menu screen
    menu_screen = Screen("Menu")
    menu_screen.add_object(GameObject(100, 100, 1, pygame.Surface((50, 50)).fill((255, 0, 0))))
    manager.add_screen(menu_screen)

    # Create game screen
    game_screen = Screen("Game")
    game_screen.add_object(GameObject(200, 150, 2, pygame.Surface((100, 100)).fill((0, 255, 0))))
    manager.add_screen(game_screen)

    # Switch to the menu screen
    manager.switch_to("Menu")

    running = True
    while running:
        dt = clock.tick(60) / 1000  # Time delta in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update and draw the current screen
        manager.update(dt)
        screen.fill((0, 0, 0))  # Clear screen
        manager.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
