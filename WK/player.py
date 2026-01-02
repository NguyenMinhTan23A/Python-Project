# player.py
import pygame
import os
from settings import *
from utils import load_gif_frames
from projectile import Projectile

class Knight(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        # ====================================================
        # 1. TẢI HÌNH ẢNH (ANIMATION)
        # ====================================================
        self.idle_frames = load_gif_frames('knight_idle.gif', KNIGHT_SIZE)
        self.walk_frames = load_gif_frames('knight_walk.gif', KNIGHT_SIZE)
        
        JUMP_SCALE = (84, 84) 
        self.jump_frames = load_gif_frames('knight_jump.gif', JUMP_SCALE)
        self.dash_frames = load_gif_frames('knight_dash.gif', JUMP_SCALE)

        THROW_SCALE = (84, 77)
        self.throw_frames = load_gif_frames('knight_throw.gif', THROW_SCALE)

        ATTACK_SCALE = (100, 90) 
        attack_1 = load_gif_frames('knight_attack_1.gif', ATTACK_SCALE)
        attack_2 = load_gif_frames('knight_attack_2.gif', ATTACK_SCALE)
        attack_3 = load_gif_frames('knight_attack_3.gif', ATTACK_SCALE)
        self.combo_list = [attack_1, attack_2, attack_3]
        
        self.heal_frames = load_gif_frames('knight_heal.gif', KNIGHT_SIZE)
        
        DEATH_SCALE = (100, 85)
        self.death_frames = load_gif_frames('knight_death.gif', DEATH_SCALE)

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # ====================================================
        # 2. TẢI ÂM THANH
        # ====================================================
        base_path = os.path.dirname(__file__)
        def load_snd(name):
            try: return pygame.mixer.Sound(os.path.join(base_path, 'assets', name))
            except: return None
            
        self.snd_slash = load_snd('slash.mp3')
        self.snd_jump = load_snd('jump.mp3')
        self.snd_throw = load_snd('throw.mp3')
        self.snd_dash = load_snd('dash.mp3')
        self.snd_heal = load_snd('heal.mp3')
        self.snd_hit = load_snd('hit.mp3')
        self.snd_death = load_snd('death.mp3')
        
        # Chỉnh âm lượng (Tùy chọn)
        if self.snd_slash: self.snd_slash.set_volume(0.5) 
        if self.snd_jump: self.snd_jump.set_volume(0.3)
        if self.snd_throw: self.snd_throw.set_volume(0.6)
        if self.snd_dash: self.snd_dash.set_volume(0.5)
        if self.snd_heal: self.snd_heal.set_volume(0.8)
        if self.snd_death: self.snd_death.set_volume(1.0)

        # ====================================================
        # 3. CÁC CHỈ SỐ (STATS)
        # ====================================================
        self.vel_y = 0
        self.facing_right = True
        self.jump_count = 0
        self.on_ground = False 
        
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 60 
        self.state = 'idle' 
        self.is_moving_x = False 

        self.hp = 100
        self.max_hp = 100
        self.alive = True
        self.invincible_timer = 0 
        
        self.ammo = START_AMMO  
        self.keys = 0  # <--- QUAN TRỌNG: Biến đếm chìa khóa
        
        self.shoot_cooldown = 0
        self.dash_timer = 0       
        self.dash_cooldown = 0
        self.combo_index = 0 
        self.combo_timer = 0 

    # ====================================================
    # 4. CÁC HÀM XỬ LÝ (LOGIC)
    # ====================================================
    def get_input(self, projectile_group):
        keys = pygame.key.get_pressed()
        if not self.alive: return
        # Nếu đang lướt, ném hoặc hồi máu thì không nhận input di chuyển
        if self.state in ['dash', 'throw', 'heal']: return

        self.is_moving_x = False 

        # Di chuyển Trái/Phải
        if keys[pygame.K_a]:
            self.facing_right = False
            self.is_moving_x = True 
        if keys[pygame.K_d]:
            self.facing_right = True
            self.is_moving_x = True 

        # Tấn công (J)
        if keys[pygame.K_j]:
            if self.state != 'attack': 
                self.state = 'attack'
                self.current_frame = 0 
                self.combo_timer = 60
                if self.snd_slash: self.snd_slash.play()

        # Bắn phi tiêu (K)
        if keys[pygame.K_k] and self.ammo > 0 and self.shoot_cooldown == 0:
            if self.state != 'throw' and self.state != 'attack':
                self.state = 'throw'
                self.current_frame = 0
                if self.snd_throw: self.snd_throw.play() 
                self.shoot(projectile_group)
            
        # Lướt (L)
        if keys[pygame.K_l] and self.dash_cooldown == 0:
            self.state = 'dash'
            self.dash_timer = DASH_DURATION 
            self.dash_cooldown = DASH_COOLDOWN 
            self.current_frame = 0
            if self.snd_dash: self.snd_dash.play()
   
    def collision_horizontal(self, tiles):
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.facing_right:
                self.rect.right = tile.rect.left
            else:
                self.rect.left = tile.rect.right

    def apply_gravity(self, tiles):
        if self.state == 'dash': return

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.on_ground = False 
        
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.vel_y > 0:
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                self.jump_count = 0 
                self.on_ground = True 
            elif self.vel_y < 0:
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

    def perform_dash(self, tiles):
        if self.dash_timer > 0:
            if self.facing_right: self.rect.x += DASH_SPEED
            else: self.rect.x -= DASH_SPEED
            
            # QUAN TRỌNG: Check va chạm ngay khi lướt để không xuyên tường
            self.collision_horizontal(tiles)
            
            self.vel_y = 0 
            if self.rect.left < 0: self.rect.left = 0
            self.dash_timer -= 1
        else:
            self.state = 'idle'
            self.vel_y = 0 

    def jump(self):
        # Chỉ nhảy được khi không đang làm hành động khác
        if self.alive and self.state not in ['attack', 'throw', 'dash', 'heal', 'death']:
            if self.on_ground or self.jump_count < MAX_JUMPS:
                self.vel_y = JUMP_FORCE
                self.jump_count += 1
                self.on_ground = False 
                if self.jump_count > 1: self.current_frame = 0 
                if self.snd_jump: self.snd_jump.play()

    def shoot(self, projectile_group):
        self.ammo -= 1 
        self.shoot_cooldown = 15 
        spawn_y = self.rect.centery
        if self.facing_right: spawn_x = self.rect.right
        else: spawn_x = self.rect.left
        shuriken = Projectile(spawn_x, spawn_y, self.facing_right)
        projectile_group.add(shuriken)

    def take_damage(self, amount):
        if self.alive and self.invincible_timer == 0:
            self.hp -= amount
            self.invincible_timer = 60 
            if self.hp > 0:
                if self.snd_hit: self.snd_hit.play()
            else:
                self.hp = 0
                self.alive = False
                self.state = 'death'
                self.current_frame = 0
                if self.snd_death: self.snd_death.play()

    def start_healing(self, amount):
        if self.alive and self.hp < self.max_hp:
            self.state = 'heal'
            self.current_frame = 0
            self.is_moving_x = False
            self.hp += amount
            if self.hp > self.max_hp: self.hp = self.max_hp
            if self.snd_heal: self.snd_heal.play()

    def get_status(self):
        if not self.alive: 
            self.state = 'death'
            return
        if self.state in ['attack', 'throw', 'dash', 'heal']: return 
        if self.on_ground:
            if self.is_moving_x: self.state = 'walk'
            else: self.state = 'idle'
        else:
            self.state = 'jump'

    def animate(self):
        current_time = pygame.time.get_ticks()
        
        # Chọn bộ khung hình dựa trên trạng thái
        if self.state == 'death': frames = self.death_frames; loop = False
        elif self.state == 'attack': frames = self.combo_list[self.combo_index]; loop = False
        elif self.state == 'throw': frames = self.throw_frames; loop = False
        elif self.state == 'heal': frames = self.heal_frames; loop = False
        elif self.state == 'dash': frames = self.dash_frames; loop = True
        elif self.state == 'jump': frames = self.jump_frames; loop = True
        elif self.state == 'walk': frames = self.walk_frames; loop = True
        else: frames = self.idle_frames; loop = True
            
        if current_time - self.last_update > self.animation_speed:
            self.last_update = current_time
            self.current_frame += 1
            if self.current_frame >= len(frames):
                if loop:
                    self.current_frame = 0
                else:
                    if self.state == 'death': self.current_frame = len(frames) - 1
                    else:
                        was_attacking = (self.state == 'attack')
                        self.state = 'idle' 
                        self.current_frame = 0
                        frames = self.idle_frames 
                        if was_attacking:
                            # Chuyển sang đòn đánh tiếp theo trong combo
                            self.combo_index += 1
                            if self.combo_index >= len(self.combo_list): self.combo_index = 0

        if len(frames) > 0:
            idx = min(self.current_frame, len(frames) - 1)
            self.image = frames[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def get_sword_rect(self):
        """Lấy Hitbox của kiếm để check va chạm với quái"""
        if self.state == 'attack' and self.alive:
            sword_w, sword_h = 55, 80 
            offset_x = 40
            offset_y = -40
            if self.facing_right:
                return pygame.Rect(self.rect.right - offset_x, self.rect.centery + offset_y, sword_w, sword_h)
            else:
                return pygame.Rect(self.rect.left - sword_w + offset_x, self.rect.centery + offset_y, sword_w, sword_h)
        return None

    # ====================================================
    # 5. HÀM UPDATE (CHẠY MỖI KHUNG HÌNH)
    # ====================================================
    def update(self, projectile_group, tiles): 
        # Giảm thời gian chờ (cooldown)
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        if self.dash_cooldown > 0: self.dash_cooldown -= 1
        if self.invincible_timer > 0: self.invincible_timer -= 1
        if self.state != 'attack':
            if self.combo_timer > 0: self.combo_timer -= 1
            else: self.combo_index = 0

        if self.alive:
            # --- KIỂM TRA RƠI VỰC ---
            if self.rect.top > SCREEN_HEIGHT:
                self.hp = 0
                self.alive = False
                self.state = 'death'
            
            # --- XỬ LÝ DI CHUYỂN ---
            self.get_input(projectile_group) 
            
            if self.state == 'dash':
                self.perform_dash(tiles)
            else:
                # Logic đi bộ (vừa đi vừa chém được, nhưng chậm lại)
                if self.is_moving_x and self.state != 'heal': 
                    current_speed = MOVE_SPEED 
                    if self.state == 'attack': current_speed = 2  
                    if self.facing_right: self.rect.x += current_speed
                    else: self.rect.x -= current_speed
                
                self.collision_horizontal(tiles)
                self.apply_gravity(tiles)
            
            self.get_status()
            
        else:
            # Nếu chết thì vẫn rơi xuống đất
            self.apply_gravity(tiles)
            
        self.animate()

    # ====================================================
    # 6. HÀM DRAW (QUAN TRỌNG: ĐÃ THÊM VÀO)
    # ====================================================
    def draw(self, screen):
        # Hiệu ứng nhấp nháy khi bất tử (bị thương)
        if self.invincible_timer > 0 and self.invincible_timer % 5 == 0:
            return 

        img_rect = self.image.get_rect()
        img_rect.midbottom = self.rect.midbottom
        img_rect.y += DRAW_OFFSET_Y 
        screen.blit(self.image, img_rect)