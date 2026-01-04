import pygame
import sys
import os
import math 
import random
import json # Thư viện lưu game
from settings import *
from player import Knight
from enemy import Enemy
from item import AmmoItem, HealthPotion, KeyItem
from tile import Tile, FinishLine
from ending import EndingScene

# --- 1. KHỞI TẠO ---
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hành trình hiệp sĩ")
clock = pygame.time.Clock()

base_path = os.path.dirname(__file__)

# Fonts
font_path = os.path.join(base_path, 'assets', 'game_font.ttf')
try:
    font_title = pygame.font.Font(font_path, 80)
    font_menu = pygame.font.Font(font_path, 40)
    font_ui = pygame.font.Font(font_path, 24)
    font_btn = pygame.font.Font(font_path, 30) 
    font_guide = pygame.font.Font(font_path, 20)
    font_key = pygame.font.Font(font_path, 28)
except:
    font_title = pygame.font.SysFont("Arial", 80, bold=True)
    font_menu = pygame.font.SysFont("Arial", 40)
    font_ui = pygame.font.SysFont("Arial", 24, bold=True)
    font_btn = pygame.font.SysFont("Arial", 30)
    font_guide = pygame.font.SysFont("Arial", 20)
    font_key = pygame.font.SysFont("Arial", 28, bold=True)

# Backgrounds
bg_path = os.path.join(base_path, 'assets', 'menu_bg.png')
try:
    menu_bg = pygame.image.load(bg_path).convert()
    menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
except: menu_bg = None

game_bg_path = os.path.join(base_path, 'assets', 'background.png')
try:
    game_bg = pygame.image.load(game_bg_path).convert()
    game_bg = pygame.transform.scale(game_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_width = game_bg.get_width()
except: game_bg = None; bg_width = SCREEN_WIDTH

# SFX
try:
    snd_key_pickup = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'key.mp3'))
    snd_level_complete = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'win.mp3'))
    snd_door_open = pygame.mixer.Sound(os.path.join(base_path, 'assets', 'door_open.mp3'))
    snd_key_pickup.set_volume(0.6)
    snd_level_complete.set_volume(0.8)
    snd_door_open.set_volume(1.0)
except:
    snd_key_pickup = None; snd_level_complete = None; snd_door_open = None

# Music
music_files = {
    'menu': os.path.join(base_path, 'assets', 'music_menu.mp3'),
    'game': os.path.join(base_path, 'assets', 'music_game.mp3'),
    'ending': os.path.join(base_path, 'assets', 'music_ending.mp3')
}
current_music_track = None 

def update_music(state):
    global current_music_track
    target_track = None
    if state in ['MENU', 'LEVEL_SELECT', 'LEVEL_COMPLETE', 'TUTORIAL', 'PAUSE']: target_track = 'menu'
    elif state == 'GAMEPLAY': target_track = 'game'
    elif state == 'ENDING_CUTSCENE': target_track = 'ending'
    
    if target_track != current_music_track:
        path = music_files.get(target_track)
        if path and os.path.exists(path):
            pygame.mixer.music.stop()
            pygame.mixer.music.load(path)
            pygame.mixer.music.set_volume(0.5) 
            pygame.mixer.music.play(-1) 
            current_music_track = target_track

# --- 2. HỆ THỐNG LƯU TRỮ (SAVE SYSTEM) ---
SAVE_FILE = "savegame.json"

def load_game_data():
    try:
        with open(SAVE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"max_level": 1, "high_scores": {}}

def save_game_data():
    data = {"max_level": max_level_unlocked, "high_scores": high_scores}
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

game_data = load_game_data()
max_level_unlocked = game_data.get("max_level", 1)
high_scores = game_data.get("high_scores", {})

# --- 3. BIẾN GAME ---
current_state = 'MENU' 
current_level_index = 0
total_keys_in_level = 0 
bg_scroll = 0 
earned_stars = 0 
ending_scene = None
current_score = 0 

# CẤU HÌNH ĐIỂM SAO (Phù hợp lượng quái vừa phải)
LEVEL_THRESHOLDS = {
    0: [300, 500, 700],   
    1: [600, 1000, 1400],   
    2: [1000, 1800, 2500], 
}
current_thresholds = [200, 500, 800] 

tile_group = pygame.sprite.Group()
finish_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
enemy_projectile_group = pygame.sprite.Group() # Nhóm đạn quái
item_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle()

# --- HÀM HỖ TRỢ VẼ ---
def draw_text(text, font, color, x, y, center=True):
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def draw_key_icon(screen, char, x, y):
    key_rect = pygame.Rect(x, y, 50, 50)
    pygame.draw.rect(screen, (50, 50, 50), (x, y+4, 50, 50), border_radius=8)
    pygame.draw.rect(screen, (240, 240, 240), key_rect, border_radius=8)
    pygame.draw.rect(screen, (20, 20, 20), key_rect, 2, border_radius=8)
    draw_text(char, font_key, (20, 20, 20), x + 25, y + 25, center=True)

def draw_star(surface, x, y, size, color):
    points = []
    for i in range(10):
        angle = math.pi / 2 + i * math.pi / 5
        r = size if i % 2 == 0 else size / 2.5
        px = x + math.cos(angle) * r
        py = y - math.sin(angle) * r
        points.append((px, py))
    pygame.draw.polygon(surface, color, points)
    pygame.draw.polygon(surface, (255, 255, 255), points, 1)

def draw_bg():
    screen.fill(SKY_BLUE) 
    if game_bg:
        width = bg_width
        tiles = math.ceil(SCREEN_WIDTH / width) + 1
        parallax_scroll = bg_scroll * 0.5
        rel_x = parallax_scroll % width
        y_offset = 40 
        for i in range(tiles):
            screen.blit(game_bg, (rel_x - width + i * width, y_offset))

# --- SETUP LEVEL (QUAN TRỌNG: CƠ CHẾ SINH QUÁI + SAFE ZONE) ---
def setup_level(level_index):
    global current_level_index, total_keys_in_level, bg_scroll, current_score, current_thresholds
    current_level_index = level_index
    layout = ALL_LEVELS[current_level_index]
    
    bg_scroll = 0 
    current_score = 0 
    current_thresholds = LEVEL_THRESHOLDS.get(level_index, [200, 500, 800])
    
    tile_group.empty(); finish_group.empty(); enemies_group.empty()
    projectile_group.empty(); item_group.empty(); player.empty()
    enemy_projectile_group.empty()
    
    total_keys_in_level = 0 
    ground_positions = [] 
    player_start_x = 0

    # 1. Duyệt Map & Setup cơ bản
    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if cell == 'X': 
                tile_group.add(Tile((x, y), TILE_SIZE))
                ground_positions.append((x, y))
            elif cell == 'F': finish_group.add(FinishLine((x, y), TILE_SIZE))
            elif cell == 'P': 
                player.add(Knight(x, y))
                player_start_x = x
            # Quái đặt cố định trong file map (giữ nguyên hoặc xóa tùy bạn)
            elif cell == 'W': enemies_group.add(Enemy(x, y, enemy_type='wolf'))
            elif cell == 'D': enemies_group.add(Enemy(x, y, enemy_type='darkknight')) 
            elif cell == 'L': enemies_group.add(Enemy(x, y, enemy_type='firelord'))
            elif cell == 'H': item_group.add(HealthPotion(x, y))
            elif cell == 'A': item_group.add(AmmoItem(x, y))
            elif cell == 'K': 
                item_group.add(KeyItem(x, y))
                total_keys_in_level += 1
    
    # 2. Lọc vị trí an toàn & Xác định giới hạn map
    SAFE_DISTANCE = 800
    valid_ground_spots = []
    max_map_x = 0 # Tìm điểm xa nhất của bản đồ
    
    for pos in ground_positions:
        gx, gy = pos
        if gx > max_map_x: max_map_x = gx
        if abs(gx - player_start_x) > SAFE_DISTANCE:
            valid_ground_spots.append(pos)

  
    # 3. THUẬT TOÁN SINH QUÁI PHÂN HÓA

    
    # A. Cấu hình hạn ngạch (Quota) cho quái mạnh theo Level
    # Format: Level: (Max DarkKnight, Max Firelord)
    STRONG_ENEMY_QUOTAS = {
        0: (0, 0),   # Level 1: Chỉ toàn Sói
        1: (1, 1),   # Level 2: Max 1 Hiệp sĩ, 1 Pháp sư
        2: (2, 2),   # Level 3: Max 2 Hiệp sĩ, 2 Pháp sư
    }
    
    # Lấy quota cho level hiện tại (Mặc định cho level cao hơn là 5, 3)
    knight_limit, firelord_limit = STRONG_ENEMY_QUOTAS.get(level_index, (5, 3))
    
    # B. Xác định "Vùng Nguy Hiểm" (Danger Zone) - 40% cuối bản đồ
    danger_zone_start = max_map_x * 0.6 
    
    # C. Tổng số lượng quái cần sinh
    total_enemies_to_spawn = 0 + level_index * 0
    
    if valid_ground_spots:
        # Xáo trộn vị trí để sinh ngẫu nhiên
        random.shuffle(valid_ground_spots)
        
        spawned_count = 0
        current_knights = 0
        current_firelords = 0
        
        for pos in valid_ground_spots:
            if spawned_count >= total_enemies_to_spawn:
                break # Đã sinh đủ số lượng
            
            spawn_x, spawn_y = pos
            enemy_type = 'wolf' # Mặc định là Sói (yếu nhất)
            
            # Logic kiểm tra "Vùng Nguy Hiểm"
            if spawn_x > danger_zone_start:
                # Ưu tiên sinh Firelord trước nếu còn slot
                if current_firelords < firelord_limit:
                    enemy_type = 'firelord'
                    current_firelords += 1
                # Sau đó đến DarkKnight
                elif current_knights < knight_limit:
                    enemy_type = 'darkknight'
                    current_knights += 1
                # Hết slot quái mạnh thì vẫn sinh Sói
            
            # --- Kiểm tra va chạm (Để không sinh đè lên nhau) ---
            test_rect = pygame.Rect(spawn_x, spawn_y - 64, 64, 64)
            is_safe = True
            for e in enemies_group:
                if e.rect.colliderect(test_rect): is_safe = False; break
            
            if is_safe:
                enemies_group.add(Enemy(spawn_x, spawn_y, enemy_type=enemy_type))
                spawned_count += 1



# --- 4. GAME LOOP ---
running = True
while running:
    update_music(current_state)
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT: 
            save_game_data()
            running = False
        
        if event.type == pygame.KEYDOWN:
            if current_state == 'MENU':
                if event.key == pygame.K_SPACE: current_state = 'LEVEL_SELECT'
                elif event.key == pygame.K_q: running = False
                elif event.key == pygame.K_h: current_state = 'TUTORIAL'
            elif current_state == 'TUTORIAL':
                if event.key == pygame.K_ESCAPE: current_state = 'MENU'
            elif current_state == 'LEVEL_SELECT':
                if event.key == pygame.K_ESCAPE: current_state = 'MENU'
            
            elif current_state == 'GAMEPLAY':
                if event.key == pygame.K_w and player.sprite.alive: player.sprite.jump()
                if event.key == pygame.K_r and not player.sprite.alive: setup_level(current_level_index)
                
                # Nút Pause
                if event.key == pygame.K_ESCAPE: current_state = 'PAUSE'
                
                if event.key == pygame.K_n: 
                    if current_level_index + 1 < len(ALL_LEVELS):
                        max_level_unlocked += 1
                        setup_level(current_level_index + 1)
            
            elif current_state == 'PAUSE':
                if event.key == pygame.K_ESCAPE: current_state = 'GAMEPLAY'

            elif current_state == 'ENDING_CUTSCENE':
                if event.key == pygame.K_ESCAPE: current_state = 'MENU'

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if current_state == 'LEVEL_SELECT':
                start_x = SCREEN_WIDTH // 2 - 250
                for i in range(len(ALL_LEVELS)):
                    btn_rect = pygame.Rect(start_x + i * 110, SCREEN_HEIGHT // 2, 80, 80)
                    if btn_rect.collidepoint(mouse_pos):
                        if i + 1 <= max_level_unlocked:
                            setup_level(i)
                            current_state = 'GAMEPLAY'
            
            elif current_state == 'PAUSE':
                resume_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60, 200, 50)
                menu_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50)
                if resume_rect.collidepoint(mouse_pos):
                    current_state = 'GAMEPLAY'
                elif menu_rect.collidepoint(mouse_pos):
                    save_game_data()
                    current_state = 'MENU'

            elif current_state == 'LEVEL_COMPLETE':
                replay_rect = pygame.Rect(SCREEN_WIDTH//2 - 160, SCREEN_HEIGHT//2 + 80, 140, 50)
                next_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, SCREEN_HEIGHT//2 + 80, 140, 50)
                if replay_rect.collidepoint(mouse_pos):
                    setup_level(current_level_index)
                    current_state = 'GAMEPLAY'
                elif next_rect.collidepoint(mouse_pos):
                    if current_level_index + 1 < len(ALL_LEVELS):
                        setup_level(current_level_index + 1)
                        current_state = 'GAMEPLAY'
                    else:
                        current_state = 'LEVEL_SELECT'

    # --- RENDER ---
    
    if current_state == 'MENU':
        if menu_bg: screen.blit(menu_bg, (0, 0))
        else: screen.fill(SKY_BLUE)
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(150); s.fill((0,0,0))
        screen.blit(s, (0,0))
        draw_text("HÀNH TRÌNH HIỆP SĨ", font_title, (255, 215, 0), SCREEN_WIDTH/2, SCREEN_HEIGHT/3)
        draw_text("Nhấn [SPACE] để Bắt đầu", font_menu, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)
        draw_text("Nhấn [H] để xem Hướng dẫn", font_menu, (200, 255, 200), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 80)
        draw_text("Nhấn [Q] để Thoát", font_menu, (200, 200, 200), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 140)

    elif current_state == 'TUTORIAL':
        screen.fill((40, 40, 60)) 
        draw_text("HƯỚNG DẪN TRÒ CHƠI", font_title, (255, 215, 0), SCREEN_WIDTH/2, 80, center=True)
        col1_x = 200; col2_x = 700; row_start = 180; row_gap = 100
        draw_text("DI CHUYỂN", font_btn, (100, 200, 255), col1_x + 80, row_start - 40)
        draw_key_icon(screen, "A", col1_x, row_start); draw_key_icon(screen, "D", col1_x + 60, row_start)
        draw_text(": Đi Trái / Phải", font_ui, (255, 255, 255), col1_x + 180, row_start + 25, center=False)
        draw_key_icon(screen, "W", col1_x + 30, row_start + row_gap)
        draw_text(": Nhảy (Có thể nhảy đôi)", font_ui, (255, 255, 255), col1_x + 180, row_start + row_gap + 25, center=False)
        draw_key_icon(screen, "L", col1_x + 30, row_start + row_gap*2)
        draw_text(": Lướt nhanh (Dash)", font_ui, (255, 255, 255), col1_x + 180, row_start + row_gap*2 + 25, center=False)
        draw_text("CHIẾN ĐẤU", font_btn, (255, 100, 100), col2_x + 50, row_start - 40)
        draw_key_icon(screen, "J", col2_x, row_start)
        draw_text(": Chém thường", font_ui, (255, 255, 255), col2_x + 80, row_start + 25, center=False)
        draw_key_icon(screen, "K", col2_x, row_start + row_gap)
        draw_text(": Bắn phi tiêu (Tốn đạn)", font_ui, (255, 255, 255), col2_x + 80, row_start + row_gap + 25, center=False)
        draw_text("Nhấn [ESC] để Quay lại", font_menu, (200, 200, 200), SCREEN_WIDTH/2, SCREEN_HEIGHT - 60)

    elif current_state == 'LEVEL_SELECT':
        screen.fill((50, 50, 80))
        draw_text("CHỌN MÀN CHƠI", font_title, (255, 255, 255), SCREEN_WIDTH/2, 150)
        draw_text("[ESC] Quay lại", font_ui, (200, 200, 200), 80, 50)
        start_x = SCREEN_WIDTH // 2 - 250
        for i in range(len(ALL_LEVELS)):
            level_num = i + 1
            btn_rect = pygame.Rect(start_x + i * 110, SCREEN_HEIGHT // 2, 80, 80)
            if level_num <= max_level_unlocked: color = (255, 215, 0); text_color = (0, 0, 0)
            else: color = (100, 100, 100); text_color = (150, 150, 150)
            pygame.draw.rect(screen, color, btn_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), btn_rect, 3, border_radius=10)
            draw_text(str(level_num), font_menu, text_color, btn_rect.centerx, btn_rect.centery)
            
            # Hiển thị điểm cao
            score_key = str(i)
            high_s = high_scores.get(score_key, 0)
            if high_s > 0:
                draw_text(f"High: {high_s}", font_ui, (255, 255, 100), btn_rect.centerx, btn_rect.bottom + 20, center=True)

    elif current_state == 'GAMEPLAY':
        world_shift = 0
        hero = player.sprite
        if hero.alive:
            if hero.rect.centerx > SCREEN_WIDTH * 2 / 3:
                if (hero.is_moving_x and hero.facing_right) or (hero.state == 'dash' and hero.facing_right):
                    hero.rect.centerx = SCREEN_WIDTH * 2 / 3
                    if hero.state == 'dash': world_shift = -DASH_SPEED
                    elif hero.state == 'attack': world_shift = -2
                    else: world_shift = -MOVE_SPEED
            elif hero.rect.centerx < SCREEN_WIDTH / 3:
                if (hero.is_moving_x and not hero.facing_right) or (hero.state == 'dash' and not hero.facing_right):
                    can_scroll = True
                    if len(tile_group) > 0:
                        if min(tile.rect.left for tile in tile_group) >= 0: can_scroll = False
                    if can_scroll:
                        hero.rect.centerx = SCREEN_WIDTH / 3
                        if hero.state == 'dash': world_shift = DASH_SPEED
                        elif hero.state == 'attack': world_shift = 2
                        else: world_shift = MOVE_SPEED
                    else: world_shift = 0
        bg_scroll += world_shift

        player.sprite.update(projectile_group, tile_group) 
        tile_group.update(world_shift); finish_group.update(world_shift)
        
        # Cập nhật quái và đạn
        enemies_group.update(world_shift, player.sprite, tile_group, enemy_projectile_group)
        enemy_projectile_group.update(world_shift)
        
        projectile_group.update(world_shift); item_group.update(world_shift)
        
        if player.sprite.keys >= total_keys_in_level:
            for finish_line in finish_group: 
                if finish_line.is_locked:
                    finish_line.unlock()
                    if snd_door_open: snd_door_open.play()

        finish_hit = pygame.sprite.spritecollide(player.sprite, finish_group, False)
        if finish_hit and not finish_hit[0].is_locked:
            if snd_level_complete: snd_level_complete.play()
            
            score_key = str(current_level_index)
            old_high = high_scores.get(score_key, 0)
            if current_score > old_high: high_scores[score_key] = current_score
            
            if current_level_index + 1 == max_level_unlocked:
                max_level_unlocked += 1
                if max_level_unlocked > len(ALL_LEVELS): max_level_unlocked = len(ALL_LEVELS)
            
            save_game_data()

            if current_level_index == len(ALL_LEVELS) - 1:
                current_state = 'ENDING_CUTSCENE'
                ending_scene = EndingScene(screen)
            else:
                if current_score >= current_thresholds[2]: earned_stars = 3    
                elif current_score >= current_thresholds[1]: earned_stars = 2  
                elif current_score >= current_thresholds[0]: earned_stars = 1  
                else: earned_stars = 1 
                current_state = 'LEVEL_COMPLETE'

        sword_rect = player.sprite.get_sword_rect()
        if sword_rect:
            for enemy in enemies_group:
                if sword_rect.colliderect(enemy.rect): 
                    if enemy.alive:
                        enemy.take_damage(20)
                        if not enemy.alive:
                            score_val = getattr(enemy, 'score_value', 50)
                            current_score += score_val
                            # Kiểm tra va chạm giữa Kiếm và tất cả Đạn đang bay
            bullets_hit = []
            for bullet in enemy_projectile_group:
                if sword_rect.colliderect(bullet.rect):
                    bullets_hit.append(bullet)
            
            # Xóa những viên đạn bị chém trúng
            for bullet in bullets_hit:
                bullet.kill() 
                # (Tùy chọn) Bạn có thể thêm âm thanh chém trúng ở đây
                # if snd_parry: snd_parry.play()

        hits = pygame.sprite.groupcollide(enemies_group, projectile_group, False, True)
        for enemy in hits: 
            if enemy.alive:
                enemy.take_damage(20)
                if not enemy.alive:
                    score_val = getattr(enemy, 'score_value', 50)
                    current_score += score_val
        
        # Người chơi dính đạn (chỉ khi không Dash)
        if player.sprite.state != 'dash':
            bullet_hits = pygame.sprite.spritecollide(player.sprite, enemy_projectile_group, True)
            if bullet_hits: player.sprite.take_damage(15)

        pygame.sprite.groupcollide(projectile_group, tile_group, True, False)
        picked_items = pygame.sprite.spritecollide(player.sprite, item_group, True)
        for item in picked_items:
            if item.item_type == 'ammo': player.sprite.ammo += AMMO_PICKUP_AMOUNT
            elif item.item_type == 'health': player.sprite.start_healing(HEALTH_PICKUP_AMOUNT)
            elif item.item_type == 'key':
                player.sprite.keys += 1
                if snd_key_pickup: snd_key_pickup.play()

        # Người chơi chạm quái (chỉ khi không Dash)
        hits = pygame.sprite.spritecollide(player.sprite, enemies_group, False)
        if hits and player.sprite.state != 'dash':
            player.sprite.contact_timer += 1
            if player.sprite.contact_timer >= 18:
                enemy_dmg = getattr(hits[0], 'damage', 20)
                player.sprite.take_damage(enemy_dmg)
                if player.sprite.invincible_timer > 0: 
                    if player.sprite.rect.centerx < hits[0].rect.centerx: player.sprite.rect.x -= 30
                    else: player.sprite.rect.x += 30
                    player.sprite.contact_timer = 0
        else: player.sprite.contact_timer = 0

        draw_bg(); tile_group.draw(screen); finish_group.draw(screen)
        item_group.draw(screen); enemies_group.draw(screen)
        for enemy in enemies_group: 
            if hasattr(enemy, 'draw_health'): enemy.draw_health(screen)
        enemy_projectile_group.draw(screen)
        player.sprite.draw(screen); projectile_group.draw(screen)

        # UI
        pygame.draw.rect(screen, RED, (20, 20, 200, 20))
        current_hp = int((player.sprite.hp / player.sprite.max_hp) * 200)
        pygame.draw.rect(screen, GREEN, (20, 20, current_hp, 20))
        pygame.draw.rect(screen, (255,255,255), (20, 20, 200, 20), 2)
        draw_text(f"Đạn: {player.sprite.ammo}", font_ui, (255, 255, 255), 70, 60, center=True)
        draw_text(f"Level: {current_level_index + 1}", font_ui, (0,0,0), SCREEN_WIDTH - 80, 20, center=True)
        
        key_ui_x = SCREEN_WIDTH - 220; key_ui_y = 50
        s = pygame.Surface((200, 40)); s.set_alpha(180); s.fill((0, 0, 0))
        screen.blit(s, (key_ui_x, key_ui_y))
        pygame.draw.rect(screen, (255, 215, 0), (key_ui_x, key_ui_y, 200, 40), 2)
        text_color = (50, 255, 50) if player.sprite.keys >= total_keys_in_level else (255, 215, 0)
        draw_text(f"Chìa khóa: {player.sprite.keys}/{total_keys_in_level}", font_ui, text_color, key_ui_x + 100, key_ui_y + 20, center=True)

        score_ui_x = SCREEN_WIDTH - 220; score_ui_y = 100 
        s2 = pygame.Surface((200, 40)); s2.set_alpha(180); s2.fill((0, 0, 0))
        screen.blit(s2, (score_ui_x, score_ui_y))
        pygame.draw.rect(screen, (0, 200, 255), (score_ui_x, score_ui_y, 200, 40), 2) 
        draw_text(f"Điểm: {current_score}", font_ui, (255, 255, 255), score_ui_x + 100, score_ui_y + 20, center=True)

        if finish_hit and finish_hit[0].is_locked:
             draw_text("CẦN TÌM THÊM CHÌA KHÓA!", font_title, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2)
        if not player.sprite.alive:
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(128); s.fill((0,0,0))
            screen.blit(s, (0,0))
            draw_text("THẤT BẠI", font_title, RED, SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 50)
            draw_text("Nhấn [R] để Chơi lại", font_menu, (255, 255, 255), SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 20)

    # --- MÀN HÌNH PAUSE ---
    elif current_state == 'PAUSE':
        draw_bg(); tile_group.draw(screen); finish_group.draw(screen); item_group.draw(screen)
        enemies_group.draw(screen); player.sprite.draw(screen)
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(180); s.fill((0,0,0))
        screen.blit(s, (0,0))
        draw_text("TẠM DỪNG", font_title, (255, 215, 0), SCREEN_WIDTH/2, 150)
        
        resume_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 60, 200, 50)
        menu_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 20, 200, 50)
        
        pygame.draw.rect(screen, (50, 200, 50), resume_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), resume_rect, 2, border_radius=10)
        draw_text("TIẾP TỤC", font_btn, (255, 255, 255), resume_rect.centerx, resume_rect.centery, center=True)
        
        pygame.draw.rect(screen, (200, 50, 50), menu_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), menu_rect, 2, border_radius=10)
        draw_text("VỀ MENU", font_btn, (255, 255, 255), menu_rect.centerx, menu_rect.centery, center=True)
        draw_text("(Tiến trình đã được lưu)", font_guide, (200, 200, 200), SCREEN_WIDTH/2, menu_rect.bottom + 30)

    elif current_state == 'LEVEL_COMPLETE':
        draw_bg(); tile_group.draw(screen); finish_group.draw(screen); player.sprite.draw(screen) 
        s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); s.set_alpha(180); s.fill((0,0,0))
        screen.blit(s, (0,0))
        panel_w, panel_h = 500, 400
        panel_x = (SCREEN_WIDTH - panel_w) // 2
        panel_y = (SCREEN_HEIGHT - panel_h) // 2
        pygame.draw.rect(screen, (30, 30, 60), (panel_x, panel_y, panel_w, panel_h), border_radius=20)
        pygame.draw.rect(screen, (255, 215, 0), (panel_x, panel_y, panel_w, panel_h), 4, border_radius=20)
        draw_text("HOÀN THÀNH!", font_title, (255, 215, 0), SCREEN_WIDTH/2, panel_y + 60, center=True)
        draw_text(f"Tổng điểm: {current_score}", font_menu, (255, 255, 255), SCREEN_WIDTH/2, panel_y + 110, center=True)
        
        score_key = str(current_level_index)
        high_s = high_scores.get(score_key, 0)
        if current_score >= high_s:
            draw_text("KỶ LỤC MỚI!", font_ui, (255, 50, 50), SCREEN_WIDTH/2, panel_y + 145, center=True)
        else:
            draw_text(f"Kỷ lục: {high_s}", font_ui, (200, 200, 200), SCREEN_WIDTH/2, panel_y + 145, center=True)

        star_start_x = SCREEN_WIDTH/2 - 100
        star_y = panel_y + 190
        for i in range(3):
            color = (255, 215, 0) if i < earned_stars else (100, 100, 100)
            draw_star(screen, star_start_x + i * 100, star_y, 40, color)
        
        next_goal = 0
        if earned_stars < 3: next_goal = current_thresholds[earned_stars]
        if next_goal > 0:
             draw_text(f"Mục tiêu tiếp theo: {next_goal}", font_ui, (150, 150, 150), SCREEN_WIDTH/2, panel_y + 240, center=True)

        replay_rect = pygame.Rect(SCREEN_WIDTH//2 - 160, panel_y + 280, 140, 50)
        next_rect = pygame.Rect(SCREEN_WIDTH//2 + 20, panel_y + 280, 140, 50)
        pygame.draw.rect(screen, (200, 50, 50), replay_rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), replay_rect, 2, border_radius=10)
        draw_text("CHƠI LẠI", font_btn, (255, 255, 255), replay_rect.centerx, replay_rect.centery, center=True)
        
        if current_level_index + 1 < len(ALL_LEVELS):
            pygame.draw.rect(screen, (50, 200, 50), next_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), next_rect, 2, border_radius=10)
            draw_text("TIẾP THEO", font_btn, (255, 255, 255), next_rect.centerx, next_rect.centery, center=True)
        else:
            pygame.draw.rect(screen, (50, 50, 200), next_rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), next_rect, 2, border_radius=10)
            draw_text("MENU", font_btn, (255, 255, 255), next_rect.centerx, next_rect.centery, center=True)
    
    elif current_state == 'ENDING_CUTSCENE':
        if ending_scene: ending_scene.update(); ending_scene.draw()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]: current_state = 'MENU'

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()