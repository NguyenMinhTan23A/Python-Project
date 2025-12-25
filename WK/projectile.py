# projectile.py
import pygame
import os # <--- Cần thêm thư viện này để tìm đường dẫn ảnh
from settings import *

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, facing_right):
        super().__init__()
        
        # --- TẢI ẢNH PHI TIÊU (MỚI) ---
        base_path = os.path.dirname(__file__)
        img_path = os.path.join(base_path, 'assets', 'shuriken.png')
        
        try:
            # Tải ảnh và xử lý nền trong suốt
            original_image = pygame.image.load(img_path).convert_alpha()
            # Chỉnh kích thước
            self.image = pygame.transform.scale(original_image, PROJECTILE_SIZE)
        except Exception as e:
            print(f"Lỗi tải ảnh shuriken: {e}")
            # Tạo hình dự phòng nếu lỗi
            self.image = pygame.Surface(PROJECTILE_SIZE)
            self.image.fill((200, 200, 200))

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        
        # Hướng bay
        if facing_right:
            self.velocity = PROJECTILE_SPEED
        else:
            self.velocity = -PROJECTILE_SPEED
            # Lật ngược ảnh phi tiêu nếu bắn sang trái (để trông hợp lý hơn)
            self.image = pygame.transform.flip(self.image, True, False)

    def update(self):
        self.rect.x += self.velocity
        # Xóa nếu bay ra khỏi màn hình
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.kill()