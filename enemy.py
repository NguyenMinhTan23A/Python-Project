# enemy.py
import pygame
import math
import random
from settings import *
from utils import load_gif_frames

# --- 1. CẤU HÌNH QUÁI VẬT ---
ENEMY_CONFIG = {
    'wolf': {
        'hp': 20,           
        'speed': 2,
        'damage': 20,
        'scale': (80, 80),
        'prefix': 'wolf',
        'attack_range': 30,
        'show_hp': False 
    },
    'knight': {             
        'hp': 100,          
        'speed': 1.5,
        'damage': 30,
        'scale': (140, 140), 
        'prefix': 'darkknight',
        'attack_range': 110, 
        'show_hp': True     
    },
    'firelord': {
        'hp': 60,           
        'speed': 1.5,
        'damage': 25,
        'scale': (80, 100),
        'prefix': 'firelord',
        'attack_range': 80,
        'show_hp': True     
    }
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance=200, enemy_type='wolf'):
        super().__init__()
        
        if enemy_type not in ENEMY_CONFIG: enemy_type = 'wolf'
        self.data = ENEMY_CONFIG[enemy_type]
        self.enemy_type = enemy_type
        
        scale = self.data['scale']
        prefix = self.data['prefix']
        
        # Bắt buộc load đúng prefix, không try...except để fallback về wolf nữa
        self.idle_frames = load_gif_frames(f'{prefix}_idle.gif', scale)
        self.walk_frames = load_gif_frames(f'{prefix}_walk.gif', scale)
        self.attack_frames = load_gif_frames(f'{prefix}_attack.gif', scale)
        self.death_frames = load_gif_frames(f'{prefix}_death.gif', scale)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y) 
        
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
        self.speed = self.data['speed']
        self.damage = self.data['damage']
        self.attack_range = self.data['attack_range']
        self.show_hp = self.data['show_hp']
        
        self.alive = True
        self.chase_speed = self.speed * 1.5
        self.velocity_y = 0
        self.facing_right = False 
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.detection_range = 300 
        
        self.state = 'idle'
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 100 
        self.attack_cooldown = 0
        self.move_direction = 0   
        self.move_timer = 0       

    def animate(self):
        current_time = pygame.time.get_ticks()
        
        if self.state == 'death': frames = self.death_frames; loop = False
        elif self.state == 'attack': frames = self.attack_frames; loop = False
        elif self.state == 'walk': frames = self.walk_frames; loop = True
        else: frames = self.idle_frames; loop = True 
        
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            self.current_frame += 1
            if self.current_frame >= len(frames):
                if loop: self.current_frame = 0
                else:
                    if self.state == 'death': self.kill() 
                    elif self.state == 'attack': self.state = 'idle'; self.current_frame = 0
        
        if len(frames) > 0:
            idx = min(self.current_frame, len(frames) - 1)
            self.image = frames[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def draw_health(self, surface):
        if not self.alive or not self.show_hp: return
        if self.hp < self.max_hp:
            bar_width = self.rect.width * 0.6 
            bar_height = 8
            x = self.rect.centerx - bar_width // 2
            y = self.rect.top - 20 
            
            pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))
            ratio = self.hp / self.max_hp
            pygame.draw.rect(surface, (0, 255, 0), (x, y, bar_width * ratio, bar_height))
            pygame.draw.rect(surface, (0, 0, 0), (x, y, bar_width, bar_height), 1)

    def apply_gravity(self, tiles):
        self.velocity_y += 0.8 
        self.rect.y += self.velocity_y
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.velocity_y > 0: self.rect.bottom = tile.rect.top; self.velocity_y = 0

    def wander_behavior(self):
        self.state = 'walk' if self.move_direction != 0 else 'idle'
        if self.move_timer <= 0:
            self.move_timer = random.randint(60, 180) 
            self.move_direction = random.choice([0, 0, 1, -1]) 
        self.move_timer -= 1
        
        if self.move_direction == 1:
            self.facing_right = True; self.rect.x += self.speed
            if self.rect.x > self.start_x + self.patrol_distance: self.move_direction = -1 
        elif self.move_direction == -1:
            self.facing_right = False; self.rect.x -= self.speed
            if self.rect.x < self.start_x - self.patrol_distance: self.move_direction = 1 

    def ai_behavior(self, player):
        if not self.alive or self.state == 'death': return
        if self.state == 'attack': return

        is_busy = False 
        if player:
            dist = math.sqrt((self.rect.centerx - player.rect.centerx)**2 + (self.rect.centery - player.rect.centery)**2)
            if dist < self.attack_range and self.attack_cooldown == 0:
                self.state = 'attack'; self.current_frame = 0
                self.attack_cooldown = 120
                self.facing_right = player.rect.centerx > self.rect.centerx
                is_busy = True 
            elif dist < self.detection_range:
                self.state = 'walk'; self.move_timer = 0 
                if self.rect.centerx < player.rect.centerx:
                    self.rect.x += self.chase_speed; self.facing_right = True
                else:
                    self.rect.x -= self.chase_speed; self.facing_right = False
                is_busy = True 
        if not is_busy: self.wander_behavior()

    def take_damage(self, amount):
        if not self.alive: return
        self.hp -= amount
        
        knockback = 15
        if self.enemy_type == 'knight': knockback = 5

        if self.facing_right: self.rect.x -= knockback
        else: self.rect.x += knockback
        
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            self.state = 'death'
            self.current_frame = 0

    def update(self, shift, player, tiles):
        self.rect.x += shift 
        self.start_x += shift 
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        self.apply_gravity(tiles)
        self.ai_behavior(player)
        self.animate()