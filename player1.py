import pygame
from object import Object
from fish import Fish

class Player(Object):
    def __init__(self, x, y, image_path):
        super().__init__(x, y, image_path)
        self.normal_speed = 0.5
        self.accelerated_speed = self.normal_speed * 2
        self.speed = self.normal_speed
        self.size = 2
        self.score = 0
        self.is_accelerating = False  # 标记是否正在加速

    def update(self):
        if self.is_accelerating:
            self.speed = self.accelerated_speed
        else:
            self.speed = self.normal_speed
    
        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction_x = (mouse_x - self.x)
        direction_y = (mouse_y - self.y)
        
        if direction_x != 0 or direction_y != 0:
            length = (direction_x ** 2 + direction_y ** 2) ** 0.5
            self.velocity_x = direction_x * self.speed / length
            self.velocity_y = direction_y * self.speed / length
        else:
            self.velocity_x = 0
            self.velocity_y = 0

        super().update()

    def accelerate(self):
        self.is_accelerating = True

    def reset_speed(self):
        self.is_accelerating = False

    def update_size(self):
        # 根据分数更新大小的逻辑
        # 例如，每达到一定分数，增加一定的大小
        if self.score >= 10:
            self.size = 3
        elif self.score >= 20:
            self.size = 4

    def get_width(self):
        return self.image.get_width()/2

    def get_height(self):
        return self.image.get_height()/2
    
    def eat(self, other_object):
        if isinstance(other_object, Fish):
            if other_object.size < self.size:
                self.size += other_object.size
                self.score += 1