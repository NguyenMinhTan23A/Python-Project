# tile.py
import pygame
import os
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'ground.png')
        
        # Bắt buộc load ảnh
        original_image = pygame.image.load(img_path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (size, size))
        
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift

class FinishLine(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        super().__init__()
        self.is_locked = True
        base_path = os.path.dirname(__file__)
        
        target_size = (GATE_WIDTH, GATE_HEIGHT)
        locked_path = os.path.join(base_path, 'assets', 'gate_locked.png')
        open_path = os.path.join(base_path, 'assets', 'gate_open.png')

        # Bắt buộc load ảnh
        img_locked = pygame.image.load(locked_path).convert_alpha()
        self.locked_image = pygame.transform.scale(img_locked, target_size)
        
        img_open = pygame.image.load(open_path).convert_alpha()
        self.open_image = pygame.transform.scale(img_open, target_size)

        self.image = self.locked_image
        self.rect = self.image.get_rect()
        
        ground_y = pos[1] + tile_size 
        self.rect.bottom = ground_y
        self.rect.left = pos[0]

    def unlock(self):
        if self.is_locked:
            self.is_locked = False
            self.image = self.open_image
            old_bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = old_bottomleft

    def update(self, x_shift):
        self.rect.x += x_shift