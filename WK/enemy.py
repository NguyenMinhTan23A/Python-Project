import pygame
import math
import random
from settings import *
from utils import load_gif_frames

# --- CẤU HÌNH QUÁI VẬT ---
ENEMY_CONFIG = {
    'wolf': {
        'hp': 30, 'speed': 2.5, 'damage': 20, 'scale': (80, 80),
        'prefix': 'wolf', 'attack_range': 30, 'show_hp': False,
        'score': 300, 'facing_right_default': True 
    },
    'darkknight': {             
        'hp': 120, 'speed': 1.2, 'damage': 35, 'scale': (140, 140), 
        'prefix': 'darkknight', 'attack_range': 110, 'show_hp': True,
        'score': 500, 'facing_right_default': True 
    },
    'firelord': {
        'hp': 80,   # Tăng máu lên 80 (trâu hơn xíu)
        'speed': 2.0, 
        'damage': 30, # Tăng damage lên 30 (đạn chậm nhưng thốn)
        'scale': (80, 100),
        'prefix': 'firelord', 
        'attack_range': 400, # Tăng tầm bắn lên 400 (Bắn từ xa)
        'show_hp': True, 'score': 750, 'facing_right_default': True 
    }
}

# --- CLASS ĐẠN CỦA QUÁI VẬT (CẦU LỬA TO VÀ CHẬM) ---
# --- CLASS ĐẠN CỦA QUÁI VẬT (CẦU LỬA ĐÃ VẼ LẠI) ---
class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y, target_x, target_y):
        super().__init__()
        
        # 1. Tăng kích thước surface lên một chút để chứa phần hào quang
        size = 36  # Kích thước tổng thể (bao gồm cả vùng sáng mờ)
        radius = size // 2
        center = (radius, radius)
        
        # Sử dụng SRCALPHA để hỗ trợ màu trong suốt
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        
        # --- VẼ CẦU LỬA MỚI (Sử dụng màu có độ trong suốt - RGBA) ---
        # Cấu trúc màu: (Red, Green, Blue, Alpha) - Alpha càng thấp càng trong suốt

        # Lớp 1: Hào quang ngoài cùng (Đỏ nhạt, rất trong suốt, to nhất)
        # Tạo cảm giác tỏa nhiệt xung quanh
        pygame.draw.circle(self.image, (200, 50, 0, 80), center, radius)

        # Lớp 2: Phần thân lửa (Cam đỏ, trong suốt vừa, nhỏ hơn lớp 1)
        pygame.draw.circle(self.image, (255, 100, 0, 150), center, radius - 4)
        
        # Lớp 3: Phần gần lõi (Cam vàng sáng, ít trong suốt hơn)
        pygame.draw.circle(self.image, (255, 180, 0, 200), center, radius - 8)

        # Lớp 4: Lõi nhiệt (Vàng trắng, đặc hoàn toàn, nhỏ nhất)
        # Tạo điểm nhấn sáng nhất ở giữa
        pygame.draw.circle(self.image, (255, 255, 200, 255), center, radius - 12)

        # -----------------------------------------------------------
        
        self.rect = self.image.get_rect(center=(x, y))
        
        # --- TỐC ĐỘ CHẬM (DỄ NÉ) ---
        self.speed = 3.0 
        
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance != 0:
            self.dx = (dx / distance) * self.speed
            self.dy = (dy / distance) * self.speed
        else:
            self.dx = self.speed; self.dy = 0
            
    def update(self, world_shift):
        self.rect.x += self.dx + world_shift
        self.rect.y += self.dy
        # Xóa đạn nếu bay ra khỏi màn hình
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or \
           self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance=200, enemy_type='wolf'):
        super().__init__()
        
        if enemy_type not in ENEMY_CONFIG: enemy_type = 'wolf'
        self.data = ENEMY_CONFIG[enemy_type]
        self.enemy_type = enemy_type
        
        scale = self.data['scale']
        prefix = self.data['prefix']
        
        # Load ảnh
        try:
            self.idle_frames = load_gif_frames(f'{prefix}_idle.gif', scale)
            self.walk_frames = load_gif_frames(f'{prefix}_walk.gif', scale)
            self.attack_frames = load_gif_frames(f'{prefix}_attack.gif', scale)
            self.death_frames = load_gif_frames(f'{prefix}_death.gif', scale)
        except:
            # Fallback
            self.idle_frames = load_gif_frames('wolf_idle.gif', scale)
            self.walk_frames = load_gif_frames('wolf_walk.gif', scale)
            self.attack_frames = load_gif_frames('wolf_attack.gif', scale)
            self.death_frames = load_gif_frames('wolf_death.gif', scale)

        # Load ảnh block cho DarkKnight
        if self.enemy_type == 'darkknight':
            try: self.block_frames = load_gif_frames(f'{prefix}_block.gif', scale)
            except: self.block_frames = self.idle_frames 
        else:
            self.block_frames = []

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x, y) 
        
        self.hp = self.data['hp']
        self.max_hp = self.data['hp']
        self.speed = self.data['speed']
        self.damage = self.data['damage']
        self.attack_range = self.data['attack_range']
        self.show_hp = self.data['show_hp']
        self.score_value = self.data.get('score', 0)
        self.facing_right_default = self.data.get('facing_right_default', False)
        
        self.alive = True
        self.chase_speed = self.speed * 1.5
        self.velocity_y = 0
        self.facing_right = False 
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.detection_range = 400 # Tăng tầm phát hiện cho Firelord
        
        self.state = 'idle'
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 100 
        self.attack_cooldown = 0
        self.move_direction = 0   
        self.move_timer = 0       
        self.is_blocking = False 
        self.block_timer = 0     

    def animate(self):
        current_time = pygame.time.get_ticks()
        
        if self.state == 'death': frames = self.death_frames; loop = False
        elif self.is_blocking and self.enemy_type == 'darkknight':
            if hasattr(self, 'block_frames') and len(self.block_frames) > 0:
                frames = self.block_frames; loop = True
            else: frames = self.idle_frames; loop = True
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
            if self.is_blocking and self.block_frames == self.idle_frames:
                 self.image = self.image.copy()
                 self.image.fill((100, 100, 255), special_flags=pygame.BLEND_RGB_ADD)
            if self.facing_right != self.facing_right_default:
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
            if self.is_blocking:
                font = pygame.font.SysFont("Arial", 12, bold=True)
                txt = font.render("BLOCK!", True, (100, 200, 255))
                surface.blit(txt, (x, y - 15))

    def apply_gravity(self, tiles):
        self.velocity_y += 0.8 
        self.rect.y += self.velocity_y
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.velocity_y > 0: self.rect.bottom = tile.rect.top; self.velocity_y = 0
            elif self.velocity_y < 0: self.rect.top = tile.rect.bottom; self.velocity_y = 0

    def check_horizontal_collision(self, tiles):
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.facing_right: 
                self.rect.right = tile.rect.left
                if self.move_direction == 1: self.move_direction = -1
            else: 
                self.rect.left = tile.rect.right
                if self.move_direction == -1: self.move_direction = 1

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

    def ai_behavior(self, player, projectile_group):
        if not self.alive or self.state == 'death': return
        if self.state == 'attack': return

        if self.enemy_type == 'darkknight':
            if self.is_blocking:
                self.block_timer -= 1
                if self.block_timer <= 0: self.is_blocking = False
                return 
            else:
                if random.random() < 0.01: 
                    self.is_blocking = True; self.block_timer = 60; self.state = 'idle'
                    return

        is_busy = False 
        if player:
            dist = math.sqrt((self.rect.centerx - player.rect.centerx)**2 + (self.rect.centery - player.rect.centery)**2)
            
            # --- AI FIRELORD (ĐÃ NÂNG CẤP) ---
            if self.enemy_type == 'firelord':
                self.facing_right = player.rect.centerx > self.rect.centerx
                
                # 1. Bị áp sát (< 200px) -> CHẠY TRỐN
                if dist < 200:
                    is_busy = True
                    self.state = 'walk'
                    if self.rect.centerx < player.rect.centerx: self.rect.x -= self.speed
                    else: self.rect.x += self.speed
                
                # 2. Trong tầm bắn (< 400px) -> ĐỨNG LẠI BẮN
                elif dist < self.attack_range:
                    is_busy = True
                    self.state = 'idle'
                    if self.attack_cooldown == 0:
                        self.state = 'attack'
                        self.attack_cooldown = 150 # 2.5 giây bắn 1 lần
                        if projectile_group is not None:
                            fireball = EnemyProjectile(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
                            projectile_group.add(fireball)
                
                # 3. Ở xa nhưng thấy -> ĐUỔI THEO
                elif dist < self.detection_range:
                     is_busy = True; self.state = 'walk'
                     if self.rect.centerx < player.rect.centerx: self.rect.x += self.speed
                     else: self.rect.x -= self.speed
            # ---------------------------------
            
            else: # AI Cận chiến
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
        if self.is_blocking: return

        self.hp -= amount
        knockback = 15
        if self.enemy_type == 'darkknight': knockback = 5

        if self.facing_right: self.rect.x -= knockback
        else: self.rect.x += knockback
        
        if self.hp <= 0:
            self.hp = 0; self.alive = False; self.state = 'death'; self.current_frame = 0

    def update(self, shift, player, tiles, enemy_projectiles=None):
        self.rect.x += shift 
        self.start_x += shift 
        if self.attack_cooldown > 0: self.attack_cooldown -= 1
        self.ai_behavior(player, enemy_projectiles)
        self.check_horizontal_collision(tiles)
        self.apply_gravity(tiles)
        self.animate()