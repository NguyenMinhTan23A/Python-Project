# item.py
import pygame
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) 

    def update(self, x_shift=0):
        self.rect.x += x_shift

class AmmoItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'ammo') 
        self.image.fill((0, 0, 255))
        pygame.draw.rect(self.image, (255, 255, 255), (10, 5, 10, 20))

class HealthPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'health') 
        self.image.fill((255, 0, 0))    
        pygame.draw.rect(self.image, (255, 255, 255), (10, 5, 10, 20))
        pygame.draw.rect(self.image, (255, 255, 255), (5, 10, 20, 10))

# --- THÊM CLASS CHÌA KHÓA ---
class KeyItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'key')
        self.image.fill((255, 255, 0)) # Màu Vàng Chanh
        # Vẽ hình chìa khóa đơn giản (cán tròn + thân dài)
        pygame.draw.circle(self.image, (0,0,0), (10, 10), 4)
        pygame.draw.line(self.image, (0,0,0), (10, 14), (20, 24), 3)