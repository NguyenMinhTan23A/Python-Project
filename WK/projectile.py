# projectile.py
import pygame
import os
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'shuriken.png')
        
        try:
            original_image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, PROJECTILE_SIZE)
        except:
            self.image = pygame.Surface(PROJECTILE_SIZE)
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        if facing_right:
            self.velocity = PROJECTILE_SPEED
        else:
            self.velocity = -PROJECTILE_SPEED
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self, x_shift=0):
        self.rect.x += self.velocity
        self.rect.x += x_shift
        
        if self.rect.right < -200 or self.rect.left > SCREEN_WIDTH + 200:
            self.kill()