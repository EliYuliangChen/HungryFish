
import pygame
from object import Object
from fish import Fish

class Player(Object):
    MAX_ACCELERATION_DISTANCE = 100  # The maximum distance the player can travel while accelerating

    def __init__(self, x, y, image_path):
        self.acceleration_distance = 0  # The distance the player has traveled while accelerating

        super().__init__(x, y, image_path)
        self.normal_speed = 5
        self.accelerated_speed = self.normal_speed * 5
        self.speed = self.normal_speed
        self.size = 1
        self.score = 0
        self.is_accelerating = False  # 标记是否正在加速
        self.is_game_over = False  # 标记游戏是否结束
        self.last_acceleration_time = None
        self.image_path = image_path
        self.prev_mouse_pos = (x, y)
        self.facing_right = True  # New attribute to track player's direction
        self.original_image = pygame.image.load(self.image_path)  # Preload the image
        if self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image  # Preload the image
        # self.flipped_image = pygame.transform.flip(self.original_image, True, False)  # Preload the flipped image
        

    def update(self):
        if self.is_game_over:
            return  # 如果游戏结束，不再更新玩家状态

        if self.is_accelerating:
            self.speed = self.accelerated_speed
            # Update the acceleration distance
            self.acceleration_distance += (self.velocity_x ** 2 + self.velocity_y ** 2) ** 0.5
            # Check if the acceleration distance has reached the maximum
            if self.acceleration_distance >= self.MAX_ACCELERATION_DISTANCE:
                self.reset_speed()
                self.acceleration_distance = 0  # Reset the acceleration distance
        else:
            self.speed = self.normal_speed

        mouse_x, mouse_y = pygame.mouse.get_pos()
        direction_x = (mouse_x - self.x)
        direction_y = (mouse_y - self.y)
        
        if abs(direction_x) < 5 or abs(direction_y) < 5:
            self.velocity_x = 0
            self.velocity_y = 0
        else:
            length = (direction_x ** 2 + direction_y ** 2) ** 0.5
            self.velocity_x = direction_x * self.speed / length
            self.velocity_y = direction_y * self.speed / length
        
            if direction_x > 10 and not self.facing_right:
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_right = True
            elif direction_x < -10 and self.facing_right:
                self.image = self.original_image
                self.facing_right = False
        
        self.update_size()
        super().update()

    def accelerate(self):
        self.is_accelerating = True

    def reset_speed(self):
        self.is_accelerating = False

    def update_size(self):
        # 根据分数更新大小的逻辑
        if self.score >= 30:
            self.size = 4
            self.image_path = 'fishSize4.png'
            self.image = pygame.image.load(self.image_path)
            self.original_image = pygame.image.load(self.image_path)
            # self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        elif self.score >= 20:
            self.size = 3
            self.image_path = 'fishSize3.png'
            self.image = pygame.image.load(self.image_path)
            self.original_image = pygame.image.load(self.image_path)
            # self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        elif self.score >= 10:
            self.size = 2
            self.image_path = 'fishSize2.png'
            self.image = pygame.image.load(self.image_path)
            self.original_image = pygame.image.load(self.image_path)
            # self.flipped_image = pygame.transform.flip(self.original_image, True, False)
        if self.facing_right:
            self.image = pygame.transform.flip(self.original_image, True, False)
        else:
            self.image = self.original_image
  
    def eat(self, other_object):
        if isinstance(other_object, Fish):
            if other_object.size <= self.size:
                self.score += 1
            else:
                self.is_game_over = True  # 设置游戏结束标志
