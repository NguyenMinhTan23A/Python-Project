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
        # PHẦN 1: TẢI HÌNH ẢNH (ĐÃ ĐIỀU CHỈNH SIZE NHỎ HƠN)
        # ====================================================
        self.idle_frames = load_gif_frames('knight_idle.gif', KNIGHT_SIZE)
        self.walk_frames = load_gif_frames('knight_walk.gif', KNIGHT_SIZE)
        
        # Tỉ lệ mới: x0.7 so với cũ
        # Cũ: (120, 120) -> Mới: (84, 84)
        JUMP_SCALE = (84, 84) 
        self.jump_frames = load_gif_frames('knight_jump.gif', JUMP_SCALE)
        self.dash_frames = load_gif_frames('knight_dash.gif', JUMP_SCALE)

        # Cũ: (120, 110) -> Mới: (84, 77)
        THROW_SCALE = (84, 77)
        self.throw_frames = load_gif_frames('knight_throw.gif', THROW_SCALE)

        # Cũ: (140, 130) -> Mới: (100, 90)
        ATTACK_SCALE = (100, 90) 
        attack_1 = load_gif_frames('knight_attack_1.gif', ATTACK_SCALE)
        attack_2 = load_gif_frames('knight_attack_2.gif', ATTACK_SCALE)
        attack_3 = load_gif_frames('knight_attack_3.gif', ATTACK_SCALE)
        self.combo_list = [attack_1, attack_2, attack_3]
        
        self.heal_frames = load_gif_frames('knight_heal.gif', KNIGHT_SIZE)
        
        # Cũ: (140, 120) -> Mới: (100, 85)
        DEATH_SCALE = (100, 85)
        self.death_frames = load_gif_frames('knight_death.gif', DEATH_SCALE)

        # Thiết lập ảnh & vị trí ban đầu
        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        
        # ====================================================
        # PHẦN 2: TẢI ÂM THANH (GIỮ NGUYÊN)
        # ====================================================
        base_path = os.path.dirname(__file__)
        try:
            self.snd_slash = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'slash.mp3'))
            self.snd_jump = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'jump.mp3'))
            self.snd_throw = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'throw.mp3'))
            self.snd_dash = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'dash.mp3'))
            self.snd_heal = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'heal.mp3'))
            self.snd_hit = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'hit.mp3'))
            self.snd_death = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'death.mp3'))
            
            self.snd_slash.set_volume(0.5) 
            self.snd_jump.set_volume(0.3)
            self.snd_throw.set_volume(0.6)
            self.snd_dash.set_volume(0.5)
            self.snd_heal.set_volume(0.8)
            self.snd_death.set_volume(1.0)
        except:
            print("Lưu ý: Không tìm thấy đầy đủ file âm thanh.")
            self.snd_slash = None
            self.snd_jump = None
            self.snd_throw = None
            self.snd_dash = None
            self.snd_heal = None
            self.snd_hit = None
            self.snd_death = None

        # ====================================================
        # PHẦN 3: CÁC CHỈ SỐ & VẬT LÝ
        # ====================================================
        self.vel_y = 0
        self.facing_right = True
        self.jump_count = 0
        self.on_ground = False 
        
        # Trạng thái
        self.current_frame = 0
        self.last_update = 0
        self.animation_speed = 60 
        self.state = 'idle' 
        self.is_moving_x = False 

        # Sinh tồn
        self.hp = 100
        self.max_hp = 100
        self.alive = True
        self.invincible_timer = 0 
        
        # Tài nguyên
        self.ammo = START_AMMO  
        self.gold = 0
        
        # Cooldowns
        self.shoot_cooldown = 0
        self.dash_timer = 0       
        self.dash_cooldown = 0
        self.combo_index = 0 
        self.combo_timer = 0 

    def get_input(self, projectile_group):
        keys = pygame.key.get_pressed()
        
        if not self.alive: return
        
        # Cho phép di chuyển khi đang chém (để làm hiệu ứng đi chậm)
        # CHỈ CHẶN: Dash, Throw, Heal
        if self.state in ['dash', 'throw', 'heal']: return

        self.is_moving_x = False 

        # --- XỬ LÝ DI CHUYỂN ---
        if keys[pygame.K_a]:
            self.facing_right = False
            self.is_moving_x = True 
        if keys[pygame.K_d]:
            self.facing_right = True
            self.is_moving_x = True 

        # --- XỬ LÝ TẤN CÔNG (SỬA LỖI Ở ĐÂY) ---
        if keys[pygame.K_j]:
            # QUAN TRỌNG: Chỉ kích hoạt nếu ĐANG KHÔNG chém
            if self.state != 'attack': 
                self.state = 'attack'
                self.current_frame = 0 
                self.combo_timer = 60
                if self.snd_slash: self.snd_slash.play()

        # --- XỬ LÝ NÉM ---
        if keys[pygame.K_k] and self.ammo > 0 and self.shoot_cooldown == 0:
            # Chỉ ném nếu đang rảnh tay
            if self.state != 'throw' and self.state != 'attack':
                self.state = 'throw'
                self.current_frame = 0
                if self.snd_throw: self.snd_throw.play() 
                self.shoot(projectile_group)
            
        # --- XỬ LÝ LƯỚT ---
        if keys[pygame.K_l] and self.dash_cooldown == 0:
            self.state = 'dash'
            self.dash_timer = DASH_DURATION 
            self.dash_cooldown = DASH_COOLDOWN 
            self.current_frame = 0
            if self.snd_dash: self.snd_dash.play()
   
    # --- CÁC HÀM VẬT LÝ (TILEMAP) ---   
    def collision_horizontal(self, tiles):
        """Xử lý va chạm ngang với tường"""
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.facing_right: # Đang đi phải đụng tường
                self.rect.right = tile.rect.left
            else: # Đang đi trái đụng tường
                self.rect.left = tile.rect.right

    def apply_gravity(self, tiles):
        """Xử lý trọng lực và va chạm dọc (Sàn/Trần)"""
        if self.state == 'dash': return

        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        
        # Mặc định là đang rơi (chưa chạm đất)
        self.on_ground = False 
        
        hits = pygame.sprite.spritecollide(self, tiles, False)
        for tile in hits:
            if self.vel_y > 0: # Rơi xuống chạm đất
                self.rect.bottom = tile.rect.top
                self.vel_y = 0
                self.jump_count = 0 
                self.on_ground = True 
            elif self.vel_y < 0: # Nhảy lên đụng trần
                self.rect.top = tile.rect.bottom
                self.vel_y = 0

    def perform_dash(self):
        if self.dash_timer > 0:
            if self.facing_right: self.rect.x += DASH_SPEED
            else: self.rect.x -= DASH_SPEED
            self.vel_y = 0 
            
            if self.rect.left < 0: self.rect.left = 0
            
            self.dash_timer -= 1
        else:
            self.state = 'idle'
            self.vel_y = 0 

    # --- CÁC HÀM HÀNH ĐỘNG ---

    def jump(self):
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
                print(f"HP: {self.hp}")
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
            if self.is_moving_x: 
                self.state = 'walk'
            else: 
                self.state = 'idle'
        else:
            self.state = 'jump'

    def animate(self):
        current_time = pygame.time.get_ticks()
        
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
                    if self.state == 'death':
                        self.current_frame = len(frames) - 1
                    else:
                        was_attacking = (self.state == 'attack')
                        self.state = 'idle' 
                        self.current_frame = 0
                        frames = self.idle_frames 
                        if was_attacking:
                            self.combo_index += 1
                            if self.combo_index >= len(self.combo_list): self.combo_index = 0

        if len(frames) > 0:
            idx = min(self.current_frame, len(frames) - 1)
            self.image = frames[idx]
            if not self.facing_right:
                self.image = pygame.transform.flip(self.image, True, False)

    def get_sword_rect(self):
        # Đã thu nhỏ tầm đánh của kiếm cho phù hợp với nhân vật nhỏ
        if self.state == 'attack' and self.alive:
            sword_w, sword_h = 55, 80 # Cũ: 70, 50
            offset_x = 40
            offset_y = -40
            if self.facing_right:
                return pygame.Rect(self.rect.right - offset_x, self.rect.centery + offset_y, sword_w, sword_h)
            else:
                return pygame.Rect(self.rect.left - sword_w + offset_x, self.rect.centery + offset_y, sword_w, sword_h)
        return None

    def update(self, projectile_group, tiles): 
        if self.shoot_cooldown > 0: self.shoot_cooldown -= 1
        if self.dash_cooldown > 0: self.dash_cooldown -= 1
        if self.invincible_timer > 0: self.invincible_timer -= 1

        if self.state != 'attack':
            if self.combo_timer > 0: self.combo_timer -= 1
            else: self.combo_index = 0

        if self.alive:
            self.get_input(projectile_group) 
            
            if self.state == 'dash':
                self.perform_dash()
            else:
                # --- LOGIC DI CHUYỂN & GIẢM TỐC ---
                # Chỉ di chuyển nếu có bấm phím VÀ không đang hồi máu
                if self.is_moving_x and self.state != 'heal': 
                    
                    # Tốc độ mặc định
                    current_speed = MOVE_SPEED 
                    
                    # Nếu đang chém -> Giảm tốc độ còn 2 (Đi chậm)
                    if self.state == 'attack':
                        current_speed = 2  
                    
                    if self.facing_right: self.rect.x += current_speed
                    else: self.rect.x -= current_speed
                # ----------------------------------

                self.collision_horizontal(tiles)
                self.apply_gravity(tiles)
                
            self.get_status()
            
        else:
            self.apply_gravity(tiles)
            
        self.animate()

    def draw(self, screen):
        # 1. Hiệu ứng nhấp nháy khi bất tử
        if self.invincible_timer > 0 and self.invincible_timer % 5 == 0:
            return 

        # 2. Tính toán vị trí vẽ ảnh (Visual)
        img_rect = self.image.get_rect()
        img_rect.midbottom = self.rect.midbottom
        
        # Xử lý Offset (Chỉnh sửa hiển thị)
        current_offset_y = DRAW_OFFSET_Y 
        if self.state == 'attack':
            current_offset_y -= 0 
        elif self.state == 'throw':
            current_offset_y -= 0
        img_rect.y += current_offset_y

        # 3. Vẽ nhân vật
        screen.blit(self.image, img_rect)

        # =================================================
        # --- DEBUG MODE: HIỆN TẦM ĐÁNH & HITBOX ---
        # =================================================
        
        # A. Vẽ khung cơ thể (Màu XANH LÁ)
        pygame.draw.rect(screen, (0, 255, 0), self.rect, 1) 
        
        # B. Vẽ tầm đánh kiếm (Màu ĐỎ)
        # Lấy hình chữ nhật của kiếm
        sword_rect = self.get_sword_rect()
        
        if sword_rect: # Nếu đang chém thì mới vẽ
            # Vẽ khung đỏ rỗng (độ dày 2 pixel)
            pygame.draw.rect(screen, (255, 0, 0), sword_rect, 2)
            
            # (Tùy chọn) Vẽ một lớp màu đỏ mờ để dễ nhìn hơn
            # s = pygame.Surface((sword_rect.width, sword_rect.height))
            # s.set_alpha(100) # Độ trong suốt
            # s.fill((255, 0, 0))
            # screen.blit(s, (sword_rect.x, sword_rect.y))