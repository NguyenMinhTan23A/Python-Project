# enemy.py
import pygame
from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((60, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        self.speed = 2
        self.direction = -1 

    def update(self, x_shift=0):
        self.rect.x += self.speed * self.direction
        self.rect.x += x_shift
        
        if self.rect.right >= SCREEN_WIDTH + 200 or self.rect.left <= -200:

            self.direction *= -1
