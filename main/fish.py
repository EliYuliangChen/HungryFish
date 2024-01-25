import pygame
import random
from object import Object

class Fish(Object):
    def __init__(self, x, y, image_path, screen_width, screen_height, size):
        super().__init__(x, y, image_path)
        self.original_image = pygame.image.load(image_path)  # Load the image once
        self.flipped_image = pygame.transform.flip(self.original_image, True, False)  # Preload the flipped image
        # Set velocity based on spawn position
        if x < 0:  # spawning from the left
            self.velocity_x = random.uniform(2, 4)  # move right
        else:  # spawning from the right
            self.velocity_x = random.uniform(-4, -2)  # move left
        self.velocity_y = 0  # No vertical movement
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.size = size
        self.alive = True
        self.direction_changed = False  # Flag to track if direction has changed
        self.change_direction_time = random.uniform(5, 10)  # Random time to change direction
        self.current_change_time = 0  # Current time counter
        self.image_path = image_path

    def update(self):
        if not self.direction_changed and self.current_change_time >= self.change_direction_time:
            if random.choice([True, False]):  # Randomly decide to change direction or not
                self.velocity_x = -self.velocity_x
                self.direction_changed = True
        
        if self.velocity_x > 0:
            self.image = pygame.transform.flip(pygame.image.load(self.image_path), True, False)
        else:
            self.image = pygame.image.load(self.image_path)

        
        if self.x < -50 or self.x > self.screen_width + 50:
            self.alive = False

        self.current_change_time += 1 / 60

        super().update()

    def draw(self, screen):
        if self.alive:  # Only draw the fish if it's alive
            super().draw(screen)



class SmallFish(Fish):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__(x, y, 'fishSize1.png', screen_width, screen_height, 1)
    
class Bass(Fish):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__(x, y, 'fishSize2.png', screen_width, screen_height, 2)

class Shark(Fish):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__(x, y, 'fishSize3.png', screen_width, screen_height, 3)

class Whale(Fish):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__(x, y, 'fishSize4.png', screen_width, screen_height, 4)
