# main.py
import pygame
import sys
import os
from settings import *
from player import Knight
from enemy import Enemy
from item import AmmoItem, HealthPotion, KeyItem
from tile import Tile, FinishLine

# --- 1. KHỞI TẠO ---
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hành trình hiệp sĩ")
clock = pygame.time.Clock()

# Assets - Font
base_path = os.path.dirname(__file__)
font_path = os.path.join(base_path, 'assets', 'game_font.ttf')
try:
    font_title = pygame.font.Font(font_path, 80)
    font_menu = pygame.font.Font(font_path, 40)
    font_ui = pygame.font.Font(font_path, 24)
except:
    font_title = pygame.font.SysFont("Arial", 80, bold=True)
    font_menu = pygame.font.SysFont("Arial", 40)
    font_ui = pygame.font.SysFont("Arial", 24, bold=True)

# Assets - Background
bg_path = os.path.join(base_path, 'assets', 'menu_bg.png')
try:
    menu_bg = pygame.image.load(bg_path).convert()
    menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
except: menu_bg = None

# Assets - Âm thanh Game (MỚI THÊM)
try:
    snd_key_pickup = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'key.mp3'))
    snd_level_complete = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'win.mp3'))
    
    snd_key_pickup.set_volume(0.6)
    snd_level_complete.set_volume(0.8)
except:
    snd_key_pickup = None
    snd_level_complete = None
    print("Cảnh báo: Không tìm thấy file key.mp3 hoặc win.mp3 trong thư mục assets")

# --- 2. BIẾN GAME ---
current_state = 'MENU' 
max_level_unlocked = 1 
current_level_index = 0
total_keys_in_level = 0 

tile_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()

def draw_text(text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def setup_level(level_index):
    global current_level_index, total_keys_in_level
    current_level_index = level_index
    layout = ALL_LEVELS[current_level_index]

    tile_group.empty()
    finish_group.empty()
    enemies_group.empty()
    projectile_group.empty()
    item_group.empty()
    player.empty()
    
    total_keys_in_level = 0 

    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if cell == 'X': tile_group.add(Tile((x, y), TILE_SIZE))
            elif cell == 'F': finish_group.add(FinishLine((x, y), TILE_SIZE))
            elif cell == 'P': 
                knight = Knight(x, y)
                knight.keys = 0 
                player.add(knight)
            elif cell == 'E': enemies_group.add(Enemy(x, y))
            elif cell == 'H': item_group.add(HealthPotion(x, y))
            elif cell == 'A': item_group.add(AmmoItem(x, y))
            elif cell == 'K': 
                item_group.add(KeyItem(x, y))
                total_keys_in_level += 1

# --- 3. GAME LOOP ---
running = True
while running:
    # INPUT
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: running = False
            
        if event.type == pygame.KEYDOWN:
            if current_state == 'MENU':
                if event.key == pygame.K_SPACE: current_state = 'LEVEL_SELECT'
                elif event.key == pygame.K_q: running = False
            
            elif current_state == 'LEVEL_SELECT':
                if event.key == pygame.K_ESCAPE: current_state = 'MENU'
            
            elif current_state == 'GAMEPLAY':
                if event.key == pygame.K_w and player.sprite.alive:
                    player.sprite.jump()
                if event.key == pygame.K_r and not player.sprite.alive:
                    setup_level(current_level_index)
                if event.key == pygame.K_ESCAPE:
                    current_state = 'LEVEL_SELECT'

        if event.type == pygame.MOUSEBUTTONDOWN and current_state == 'LEVEL_SELECT':
            mouse_pos = pygame.mouse.get_pos()
            start_x = SCREEN_WIDTH // 2 - 250
            for i in range(len(ALL_LEVELS)):
                btn_rect = pygame.Rect(start_x + i * 110, SCREEN_HEIGHT // 2, 80, 80)
                if btn_rect.collidepoint(mouse_pos):
                    if i + 1 <= max_level_unlocked:
                        setup_level(i)
                        current_state = 'GAMEPLAY'

    # LOGIC & DRAW
    if current_state == 'MENU':
        if menu_bg: screen.blit(menu_bg, (0, 0))
        else: screen.fill((30, 30, 30))
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(150); s.fill((0,0,0))
        screen.blit(s, (0,0))

        draw_text("HÀNH TRÌNH HIỆP SĨ", font_title, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        draw_text("Nhấn [SPACE] để Chọn Màn Chơi", font_menu, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40)
        draw_text("Nhấn [Q] để Thoát", font_menu, (200, 200, 200), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100)

    elif current_state == 'LEVEL_SELECT':
        screen.fill((50, 50, 80))
        draw_text("CHỌN MÀN CHƠI", font_title, (255, 255, 255), SCREEN_WIDTH/2, 150)
        draw_text("[ESC] Quay lại", font_ui, (200, 200, 200), 80, 50)

        start_x = SCREEN_WIDTH // 2 - 250
        for i in range(len(ALL_LEVELS)):
            level_num = i + 1
            btn_rect = pygame.Rect(start_x + i * 110, SCREEN_HEIGHT // 2, 80, 80)
            if level_num <= max_level_unlocked:
                color = (255, 215, 0)
                text_color = (0, 0, 0)
            else:
                color = (100, 100, 100)
                text_color = (150, 150, 150)
            
            pygame.draw.rect(screen, color, btn_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 3, border_radius=10)
            draw_text(str(level_num), font_menu, text_color, btn_rect.centerx, btn_rect.centery)

    elif current_state == 'GAMEPLAY':
        # Camera
        world_shift = 0
        hero = player.sprite
        if hero.alive:
            if hero.rect.centerx > SCREEN_WIDTH * 2 / 3 and hero.is_moving_x and hero.facing_right:
                world_shift = -MOVE_SPEED
                if hero.state == 'attack': world_shift = -2
                hero.speed = 0
                hero.rect.centerx = SCREEN_WIDTH * 2 / 3
            elif hero.rect.centerx < SCREEN_WIDTH / 3 and hero.is_moving_x and not hero.facing_right:
                can_scroll = True
                if len(tile_group) > 0:
                    if min(tile.rect.left for tile in tile_group) >= 0: can_scroll = False
                if can_scroll:
                    world_shift = MOVE_SPEED
                    if hero.state == 'attack': world_shift = 2
                    hero.speed = 0
                    hero.rect.centerx = SCREEN_WIDTH / 3
                else: world_shift = 0

        # Update
        player.sprite.update(projectile_group, tile_group) 
        tile_group.update(world_shift)
        finish_group.update(world_shift)
        enemies_group.update(world_shift)
        projectile_group.update(world_shift)
        item_group.update(world_shift)
        
        # MỞ KHÓA CỔNG
        if player.sprite.keys >= total_keys_in_level:
            for finish_line in finish_group:
                finish_line.unlock() 

        # XỬ LÝ KHI CHẠM ĐÍCH
        finish_hit = pygame.sprite.spritecollide(player.sprite, finish_group, False)
        if finish_hit:
            if not finish_hit[0].is_locked:
                # --- PHÁT ÂM THANH CHIẾN THẮNG ---
                if snd_level_complete: snd_level_complete.play()
                # ---------------------------------
                
                if current_level_index + 1 == max_level_unlocked:
                    max_level_unlocked += 1
                    if max_level_unlocked > len(ALL_LEVELS): max_level_unlocked = len(ALL_LEVELS)
                current_state = 'LEVEL_SELECT'
            else:
                pass

        sword_rect = player.sprite.get_sword_rect()
        if sword_rect:
            for enemy in enemies_group:
                if sword_rect.colliderect(enemy.rect): enemy.kill()
        
        pygame.sprite.groupcollide(projectile_group, enemies_group, True, True)
        pygame.sprite.groupcollide(projectile_group, tile_group, True, False)
        
        picked_items = pygame.sprite.spritecollide(player.sprite, item_group, True)
        for item in picked_items:
            if item.item_type == 'ammo': player.sprite.ammo += AMMO_PICKUP_AMOUNT
            elif item.item_type == 'health': player.sprite.start_healing(HEALTH_PICKUP_AMOUNT)
            elif item.item_type == 'key':
                player.sprite.keys += 1
                # --- PHÁT ÂM THANH NHẶT CHÌA ---
                if snd_key_pickup: snd_key_pickup.play()
                # ------------------------------

        if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
            player.sprite.take_damage(20)

        # Draw
        screen.fill(SKY_BLUE)
        tile_group.draw(screen)
        finish_group.draw(screen)
        item_group.draw(screen)
        enemies_group.draw(screen)
        player.sprite.draw(screen)
        projectile_group.draw(screen)

        # UI
        pygame.draw.rect(screen, RED, (20, 20, 200, 20))
        current_hp = int((player.sprite.hp / player.sprite.max_hp) * 200)
        pygame.draw.rect(screen, GREEN, (20, 20, current_hp, 20))
        pygame.draw.rect(screen, (255,255,255), (20, 20, 200, 20), 2)
        
        draw_text(f"Đạn: {player.sprite.ammo}", font_ui, (255, 255, 255), 70, 60, center=True)
        draw_text(f"Level: {current_level_index + 1}", font_ui, (0,0,0), SCREEN_WIDTH - 80, 30, center=True)
        
        # UI CHÌA KHÓA NỔI BẬT
        key_ui_width = 200
        key_ui_height = 40
        key_ui_x = SCREEN_WIDTH - 220
        key_ui_y = 40
        s = pygame.Surface((key_ui_width, key_ui_height))
        s.set_alpha(180) 
        s.fill((0, 0, 0))
        screen.blit(s, (key_ui_x, key_ui_y))
        pygame.draw.rect(screen, (255, 215, 0), (key_ui_x, key_ui_y, key_ui_width, key_ui_height), 2)
        key_status = f"Chìa khóa: {player.sprite.keys}/{total_keys_in_level}"
        text_color = (50, 255, 50) if player.sprite.keys >= total_keys_in_level else (255, 215, 0)
        draw_text(key_status, font_ui, text_color, key_ui_x + key_ui_width//2, key_ui_y + key_ui_height//2, center=True)

        if finish_hit and finish_hit[0].is_locked:
             draw_text("CẦN TÌM THÊM CHÌA KHÓA!", font_title, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

        if not player.sprite.alive:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(128); s.fill((0,0,0))
            screen.blit(s, (0,0))
            draw_text("THẤT BẠI", font_title, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
            draw_text("Nhấn [R] để Chơi lại", font_menu, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
            draw_text("Nhấn [ESC] để Thoát", font_menu, (200, 200, 200), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 70)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()