# tile.py
import pygame
import os
from settings import * # Đảm bảo đã import GATE_WIDTH, GATE_HEIGHT

# --- CLASS ĐẤT (Giữ nguyên không đổi) ---
class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'ground.png')
        
        try:
            original_image = pygame.image.load(img_path).convert_alpha()
            self.image = pygame.transform.scale(original_image, (size, size))
        except Exception as e:
            self.image = pygame.Surface((size, size))
            self.image.fill(BROWN)
            pygame.draw.rect(self.image, GREEN, (0, 0, size, 5))
        
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        self.rect.x += x_shift

# --- CẬP NHẬT CLASS CỔNG ĐÍCH (TO HƠN) ---
class FinishLine(pygame.sprite.Sprite):
    def __init__(self, pos, tile_size):
        # pos: là tọa độ góc trên-trái của ô đất chứa chữ 'F' (kích thước 50x50)
        super().__init__()
        self.is_locked = True
        base_path = os.path.dirname(__file__)
        
        # --- 1. TẢI ẢNH VỚI KÍCH THƯỚC MỚI (TO HƠN) ---
        locked_path = os.path.join(base_path, 'assets', 'gate_locked.png')
        open_path = os.path.join(base_path, 'assets', 'gate_open.png')
        
        # Sử dụng GATE_WIDTH và GATE_HEIGHT từ settings.py
        target_size = (GATE_WIDTH, GATE_HEIGHT)

        try:
            img_locked = pygame.image.load(locked_path).convert_alpha()
            self.locked_image = pygame.transform.scale(img_locked, target_size)
            
            img_open = pygame.image.load(open_path).convert_alpha()
            self.open_image = pygame.transform.scale(img_open, target_size)
            
        except Exception as e:
            print(f"Lỗi tải ảnh cổng: {e}. Dùng hình khối thay thế.")
            self.locked_image = pygame.Surface(target_size)
            self.locked_image.fill(RED)
            self.open_image = pygame.Surface(target_size)
            self.open_image.fill((255, 215, 0)) 

        # --- 2. THIẾT LẬP VỊ TRÍ (QUAN TRỌNG) ---
        self.image = self.locked_image
        self.rect = self.image.get_rect()

        # Logic căn chỉnh:
        # 'pos' là góc trên-trái của ô 'F' nhỏ (50x50).
        # Chúng ta muốn chân của cổng to nằm ở đáy của ô 'F' đó.
        
        # Tọa độ Y của mặt đất tại ô 'F'
        ground_y = pos[1] + tile_size 
        
        # Đặt đáy của cổng to trùng với mặt đất
        self.rect.bottom = ground_y
        # Đặt cạnh trái của cổng trùng với cạnh trái ô 'F'
        self.rect.left = pos[0]

    def unlock(self):
        """Hàm mở khóa cổng"""
        if self.is_locked:
            self.is_locked = False
            self.image = self.open_image
            # Cập nhật lại rect để đảm bảo vị trí không đổi sau khi đổi ảnh
            old_bottomleft = self.rect.bottomleft
            self.rect = self.image.get_rect()
            self.rect.bottomleft = old_bottomleft

    def update(self, x_shift):
        self.rect.x += x_shift