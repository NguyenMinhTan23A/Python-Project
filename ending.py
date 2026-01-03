# ending.py
import pygame
import os
from settings import *
from utils import load_gif_frames

class EndingScene:
    def __init__(self, screen):
        self.screen = screen
        base_path = os.path.dirname(__file__)
        
        # 1. TẢI ẢNH NỀN (Bắt buộc)
        bg_path = os.path.join(base_path, 'assets', 'ending_bg.png')
        img = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # 2. TẢI FONT (Bắt buộc)
        font_path = os.path.join(base_path, 'assets', 'game_font.ttf')
        self.font = pygame.font.Font(font_path, 32)
        self.font_big = pygame.font.Font(font_path, 60)
        self.font_hint = pygame.font.Font(font_path, 20) 
        
        # 3. CẤU HÌNH KÍCH THƯỚC LỚN
        self.BIG_KNIGHT_SIZE = (200, 200)
        self.BIG_WIFE_SIZE = (140, 180) 
        
        self.stage = 0
        self.timer = 0
        
        # 4. LOAD HIỆP SĨ & VỢ (Bắt buộc)
        self.knight_frames = load_gif_frames('knight_walk.gif', self.BIG_KNIGHT_SIZE)
        self.knight_idle = load_gif_frames('knight_idle.gif', self.BIG_KNIGHT_SIZE)
        self.knight_img = self.knight_frames[0]
        
        ground_level = SCREEN_HEIGHT - TILE_SIZE * 2
        self.knight_x = -200 
        self.knight_y = ground_level - self.BIG_KNIGHT_SIZE[1] + 25 
        
        self.knight_frame_index = 0
        
        self.wife_frames = load_gif_frames('wife_idle.gif', self.BIG_WIFE_SIZE)
        self.wife_img = self.wife_frames[0]
        self.wife_x = SCREEN_WIDTH * 2 // 3 
        self.wife_y = ground_level - self.BIG_WIFE_SIZE[1] + 25
        self.wife_frame_index = 0

        # KỊCH BẢN HỘI THOẠI
        self.dialogues = [
            (0, "Hỡi nàng! Ta đã vượt qua ngàn trùng nguy hiểm để đến đây."),
            (1, "Chàng đã đến rồi! Em biết chàng sẽ không bỏ rơi em mà."),
            (0, "Lũ quái vật kia không thể ngăn cản tình yêu của chúng ta."),
            (1, "Cảm ơn chàng, người hùng dũng cảm của đời em."),
            (0, "Nào, chúng ta hãy cùng nhau trở về nhà."),
            (1, "Vâng, cùng nhau đi đến cuối chân trời!")
        ]
        self.dialogue_index = 0

    def update(self):
        self.timer += 1
        
        if self.stage == 0:
            self.knight_x += 4
            if self.timer % 10 == 0:
                self.knight_frame_index = (self.knight_frame_index + 1) % len(self.knight_frames)
                self.knight_img = self.knight_frames[self.knight_frame_index]
            
            if self.knight_x >= self.wife_x - 180: 
                self.stage = 1
                self.knight_img = self.knight_idle[0] 

        elif self.stage == 1:
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            
            if self.timer > 30: 
                if keys[pygame.K_SPACE] or mouse[0]:
                    self.dialogue_index += 1
                    self.timer = 0 
                    if self.dialogue_index >= len(self.dialogues):
                        self.stage = 2 

        elif self.stage == 2:
            moved = False
            stop_distance = self.BIG_WIFE_SIZE[0] - 20
            
            if self.knight_x < self.wife_x - stop_distance: 
                self.knight_x += 2
                moved = True
            
            if self.wife_x > self.knight_x + stop_distance:
                self.wife_x -= 2
                moved = True
                
            if not moved:
                self.stage = 3 

        elif self.stage == 3:
            pass 

    def draw(self):
        if self.bg_image:
            self.screen.blit(self.bg_image, (0, 0))
        
        rect_k = self.knight_img.get_rect(topleft=(self.knight_x, self.knight_y))
        self.screen.blit(self.knight_img, rect_k)
        
        img_w = pygame.transform.flip(self.wife_img, False, False)
        rect_w = img_w.get_rect(topleft=(self.wife_x, self.wife_y))
        self.screen.blit(img_w, rect_w)

        if self.stage == 1 and self.dialogue_index < len(self.dialogues):
            speaker, text = self.dialogues[self.dialogue_index]
            
            panel_height = 140
            panel_rect = pygame.Rect(100, SCREEN_HEIGHT - panel_height - 20, SCREEN_WIDTH - 200, panel_height)
            
            pygame.draw.rect(self.screen, (0, 0, 0), panel_rect, border_radius=10)
            pygame.draw.rect(self.screen, (255, 255, 255), panel_rect, 3, border_radius=10)
            
            name = "Hiệp Sĩ" if speaker == 0 else "Nàng"
            name_color = (100, 200, 255) if speaker == 0 else (255, 150, 200)
            
            img_name = self.font.render(name, True, name_color)
            self.screen.blit(img_name, (panel_rect.x + 30, panel_rect.y + 20))
            
            img_text = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(img_text, (panel_rect.x + 30, panel_rect.y + 65))
            
            hint = self.font_hint.render("[Nhấn Space để tiếp tục]", True, (150, 150, 150))
            self.screen.blit(hint, (panel_rect.right - 250, panel_rect.bottom - 30))

        if self.stage == 3:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(150)
            s.fill((0,0,0))
            self.screen.blit(s, (0,0))
            
            text_1 = self.font_big.render("CẢM ƠN BẠN ĐÃ CHƠI!", True, (255, 215, 0))
            rect_1 = text_1.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50))
            self.screen.blit(text_1, rect_1)
            
            text_2 = self.font.render("Game Design by Quang Tân Tiên Thi Kiệt", True, (255, 255, 255))
            rect_2 = text_2.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20))
            self.screen.blit(text_2, rect_2)
            
            pygame.draw.circle(self.screen, (255, 50, 50), (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150), 40)
            pygame.draw.circle(self.screen, (255, 50, 50), (SCREEN_WIDTH//2 - 35, SCREEN_HEIGHT//2 - 180), 30)
            pygame.draw.circle(self.screen, (255, 50, 50), (SCREEN_WIDTH//2 + 35, SCREEN_HEIGHT//2 - 180), 30)