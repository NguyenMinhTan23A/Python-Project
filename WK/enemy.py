import pygame
import math
from settings import *
from utils import load_gif_frames

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, patrol_distance=200):
            super().__init__()
            
            # ====================================================
            # PHẦN 1: TẢI HÌNH ẢNH (SỬ DỤNG LOAD_GIF_FRAMES)
            # ====================================================
            # Định nghĩa kích thước quái vật (Bạn có thể chỉnh lại trong settings)
            self.ENEMY_SCALE = (80, 80) 
            
            # Tải các bộ ảnh động (GIF)
            # Đảm bảo bạn có các file này trong thư mục assets
            self.idle_frames = load_gif_frames('wolf_idle.gif', self.ENEMY_SCALE)
            self.walk_frames = load_gif_frames('wolf_walk.gif', self.ENEMY_SCALE)
            self.attack_frames = load_gif_frames('wolf_attack.gif', self.ENEMY_SCALE)
            self.death_frames = load_gif_frames('wolf_death.gif', self.ENEMY_SCALE)
            
            # Thiết lập ảnh ban đầu
            self.image = self.idle_frames[0]
            self.rect = self.image.get_rect()
            self.rect.bottomleft = (x, y) # Đặt vị trí chân
            
            # ====================================================
            # PHẦN 2: CHỈ SỐ & TRẠNG THÁI
            # ====================================================
            # Sinh tồn
            self.hp = 50
            self.max_hp = 50
            self.alive = True
            
            # Di chuyển
            self.speed = 2
            self.chase_speed = 3.5
            self.velocity_y = 0
            self.facing_right = False # Mặc định nhìn sang trái
            
            # AI & Phạm vi
            self.start_x = x
            self.patrol_distance = patrol_distance
            self.detection_range = 300 # Tầm nhìn
            self.attack_range = 50     # Tầm đánh
            
            # Animation & Cooldown
            self.state = 'idle'
            self.current_frame = 0
            self.last_update = 0
            self.animation_speed = 100 # Miliseconds
            self.attack_cooldown = 0
            
            # Thêm âm thanh nếu cần (Tương tự Player)
            # self.snd_hit = ...
            # ... (Sau khi load các frames) ...
            print(f"Idle frames: {len(self.idle_frames)}")
            print(f"Walk frames: {len(self.walk_frames)}")
            print(f"Attack frames: {len(self.attack_frames)}")

    def animate(self):
            """Hàm xử lý chuyển đổi ảnh động tương tự Player"""
            current_time = pygame.time.get_ticks()
            
            # Xác định bộ ảnh dựa trên trạng thái
            if self.state == 'death': frames = self.death_frames; loop = False
            elif self.state == 'attack': frames = self.attack_frames; loop = False
            elif self.state == 'walk': frames = self.walk_frames; loop = True
            else: frames = self.idle_frames; loop = True # Default is idle
            
            # Xử lý chuyển frame theo thời gian
            if current_time - self.last_update > self.animation_speed:
                self.last_update = current_time
                self.current_frame += 1
                
                # Xử lý vòng lặp
                if self.current_frame >= len(frames):
                    if loop:
                        self.current_frame = 0
                    else:
                        # Nếu là hành động không lặp (Chết/Tấn công)
                        if self.state == 'death':
                            self.current_frame = len(frames) - 1
                            self.kill() # Xóa khỏi game sau khi chết xong animation
                        elif self.state == 'attack':
                            self.state = 'idle' # Đánh xong thì đứng yên
                            self.current_frame = 0
            
            # Cập nhật ảnh hiện tại
            if len(frames) > 0:
                idx = min(self.current_frame, len(frames) - 1)
                self.image = frames[idx]
                
                # Lật ảnh nếu hướng nhìn thay đổi
                if self.facing_right:
                    self.image = pygame.transform.flip(self.image, True, False)

    def apply_gravity(self, tiles): # <--- Thêm tham số 'tiles'
        """Xử lý trọng lực và va chạm với đất"""
        self.velocity_y += 0.8 # Trọng lực
        self.rect.y += self.velocity_y
        
        # --- KIỂM TRA VA CHẠM VỚI ĐẤT (TILES) ---
        # Kiểm tra xem quái vật có chạm vào khối đất nào không
        hits = pygame.sprite.spritecollide(self, tiles, False)
        
        for tile in hits:
            if self.velocity_y > 0: # Đang rơi xuống
                self.rect.bottom = tile.rect.top # Đặt chân lên mặt gạch
                self.velocity_y = 0 # Ngừng rơi
            
            # (Tùy chọn) Xử lý va chạm trần nếu quái vật biết nhảy
            # elif self.velocity_y < 0:
            #     self.rect.top = tile.rect.bottom
            #     self.velocity_y = 0

    def ai_behavior(self, player):
            """Trí tuệ nhân tạo: Tuần tra -> Đuổi theo -> Tấn công"""
            # Kiểm tra sống chết
            if not self.alive or self.state == 'death': return
            # Nếu đang tấn công thì đứng lại (không vừa đi vừa đánh)
            if self.state == 'attack': return

            # --- BIẾN CỜ QUAN TRỌNG ---
            # Mặc định là quái vật "rảnh rỗi" (không bận đuổi hay đánh ai)
            is_busy = False 

            # --- BƯỚC 1: KIỂM TRA PLAYER CÓ TỒN TẠI KHÔNG ---
            if player: 
                # Dòng tính toán này BẮT BUỘC phải thụt vào trong if player
                distance_to_player = math.sqrt((self.rect.centerx - player.rect.centerx)**2 + (self.rect.centery - player.rect.centery)**2)
                
                # 1. LOGIC TẤN CÔNG (Nếu đủ gần)
                if distance_to_player < self.attack_range and self.attack_cooldown == 0:
                    self.state = 'attack'
                    self.current_frame = 0
                    self.attack_cooldown = 120 
                    if player.rect.centerx > self.rect.centerx: self.facing_right = True
                    else: self.facing_right = False
                    
                    is_busy = True # Đánh dấu là đang BẬN tấn công

                # 2. LOGIC ĐUỔI THEO (Nếu nhìn thấy nhưng chưa đủ gần để đánh)
                elif distance_to_player < self.detection_range:
                    self.state = 'walk'
                    if self.rect.centerx < player.rect.centerx:
                        self.rect.x += self.chase_speed
                        self.facing_right = True
                    else:
                        self.rect.x -= self.chase_speed
                        self.facing_right = False
                    
                    is_busy = True # Đánh dấu là đang BẬN đuổi theo
            
            # --- BƯỚC 2: LOGIC TUẦN TRA ---
            # Chỉ chạy khi KHÔNG bận (tức là: Hoặc không có player, Hoặc player ở quá xa)
            if not is_busy:
                self.state = 'walk'
                if self.facing_right:
                    self.rect.x += self.speed
                    # Quay đầu nếu đi quá xa điểm xuất phát
                    if self.rect.x > self.start_x + self.patrol_distance:
                        self.facing_right = False
                else:
                    self.rect.x -= self.speed
                    # Quay đầu nếu đi quá xa về bên trái
                    if self.rect.x < self.start_x - self.patrol_distance:
                        self.facing_right = True
    def take_damage(self, amount):
            """Nhận sát thương từ Player"""
            self.hp -= amount
            # Hiệu ứng đẩy lùi nhẹ
            if self.facing_right: self.rect.x -= 20
            else: self.rect.x += 20
            
            if self.hp <= 0:
                self.hp = 0
                self.alive = False
                self.state = 'death'
                self.current_frame = 0

    def update(self, player=None, tiles=None): # <--- Thêm tham số 'tiles'
        """Hàm cập nhật chính"""
        # Giảm hồi chiêu
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
            
        # Truyền danh sách tiles vào hàm trọng lực
        if tiles:
            self.apply_gravity(tiles)
        else:
            # Fallback: Nếu không có tiles thì dùng logic cũ (FLOOR_Y)
            self.velocity_y += 0.8
            self.rect.y += self.velocity_y
            if self.rect.bottom >= FLOOR_Y:
                self.rect.bottom = FLOOR_Y
                self.velocity_y = 0

        self.ai_behavior(player)
        self.animate()
