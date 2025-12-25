# item.py
import pygame
from settings import *

# --- CLASS CHA (Dùng làm khuôn mẫu) ---
class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type # Lưu loại item ('ammo', 'health', 'coin')
        self.image = pygame.Surface((30, 30))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.rect.bottom = FLOOR_Y # Luôn nằm trên đất

# --- CÁC CLASS CON (Kế thừa từ Item) ---

class AmmoItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'ammo') # Đánh dấu loại là 'ammo'
        self.image.fill((0, 0, 255))   # Màu Xanh Dương
        # Vẽ chữ A
        pygame.draw.rect(self.image, (255, 255, 255), (10, 5, 10, 20))

class HealthPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'health') # Đánh dấu loại là 'health'
        self.image.fill((255, 0, 0))     # Màu Đỏ
        # Vẽ hình chữ thập (+)
        pygame.draw.rect(self.image, (255, 255, 255), (10, 5, 10, 20))
        pygame.draw.rect(self.image, (255, 255, 255), (5, 10, 20, 10))

class Coin(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'coin')   # Đánh dấu loại là 'coin'
        self.image.fill((255, 215, 0))   # Màu Vàng
        # Vẽ hình tròn tiền xu
        pygame.draw.circle(self.image, (255, 255, 0), (15, 15), 10)