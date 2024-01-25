import pygame

class Object:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.velocity_x = 0
        self.velocity_y = 0

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def get_width(self):
        return self.image.get_width()

    def get_height(self):
        return self.image.get_height()/2
