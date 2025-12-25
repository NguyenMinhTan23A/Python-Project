# tile.py
import pygame
import os
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, size):
        super().__init__()
        
        # --- TẢI ẢNH ĐẤT (MỚI) ---
        base_path = os.path.dirname(__file__)
        # Đảm bảo bạn đã có file ground.png trong thư mục assets
        img_path = os.path.join(base_path, 'assets', 'ground.png')
        
        try:
            # Tải ảnh và xử lý trong suốt (nếu có)
            original_image = pygame.image.load(img_path).convert_alpha()
            
            # Co giãn ảnh cho vừa khít kích thước ô đất (TILE_SIZE)
            self.image = pygame.transform.scale(original_image, (size, size))
            
        except Exception as e:
            print(f"Lỗi tải ảnh đất (ground.png): {e}")
            # Nếu không tìm thấy ảnh thì dùng lại ô vuông màu nâu như cũ (Backup)
            self.image = pygame.Surface((size, size))
            self.image.fill(BROWN)
            pygame.draw.rect(self.image, GREEN, (0, 0, size, 5)) # Vẽ cỏ giả
        
        # Tạo khung va chạm
        self.rect = self.image.get_rect(topleft=pos)

    def update(self, x_shift):
        # Dành cho Camera sau này
        self.rect.x += x_shift