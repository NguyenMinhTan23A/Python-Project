# enemy.py
import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Tạm thời dùng hình vuông đỏ (Sau này bạn có thể dùng load_gif_frames như player)
        self.image = pygame.Surface((60, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect.bottom = FLOOR_Y # Luôn đứng trên đất
        
        self.speed = 2
        self.direction = -1 # -1 là đi sang trái, 1 là sang phải

    def update(self):
        # Quái vật tự đi qua đi lại
        self.rect.x += self.speed * self.direction
        
        # Chạm tường thì quay đầu
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1