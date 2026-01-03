# item.py
import pygame
import os
from settings import *

class Item(pygame.sprite.Sprite):
    def __init__(self, x, y, item_type):
        super().__init__()
        self.item_type = item_type
        self.image = None
        self.rect = None

    def update(self, x_shift=0):
        self.rect.x += x_shift

class AmmoItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'ammo') 
        
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'ammo.png')
        ITEM_SIZE = (30, 30)

        # Bắt buộc load ảnh
        original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, ITEM_SIZE)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class HealthPotion(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'health') 
        
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'potion.png')
        ITEM_SIZE = (30, 30)

        # Bắt buộc load ảnh
        original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, ITEM_SIZE)
            
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class KeyItem(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 'key')
        
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'key.png')
        KEY_SIZE = (40, 40)
        
        # Bắt buộc load ảnh
        original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, KEY_SIZE)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)