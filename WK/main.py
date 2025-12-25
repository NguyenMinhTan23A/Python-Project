# main.py
import pygame
import sys
from settings import *
from player import Knight
from enemy import Enemy
from item import AmmoItem, HealthPotion, Coin
from tile import Tile # <--- Import mới

# KHỞI TẠO
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level 1: Mario Style")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24, bold=True)

# --- CÁC GROUP ---
# Tạo nhóm chứa Đất
tile_group = pygame.sprite.Group()
enemies_group = pygame.sprite.Group()
projectile_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
player = pygame.sprite.GroupSingle() # Dùng GroupSingle cho tiện quản lý player

# --- HÀM SETUP LEVEL (Đọc bản đồ) ---
def setup_level(layout):
    for row_index, row in enumerate(layout):
        for col_index, cell in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            
            if cell == 'X':
                tile = Tile((x, y), TILE_SIZE)
                tile_group.add(tile)
            elif cell == 'P':
                player_sprite = Knight(x, y)
                player.add(player_sprite)
            elif cell == 'E':
                enemies_group.add(Enemy(x, y))
            elif cell == 'C':
                item_group.add(Coin(x, y))
            elif cell == 'H':
                item_group.add(HealthPotion(x, y))
            elif cell == 'A':
                item_group.add(AmmoItem(x, y))

# GỌI HÀM SETUP
setup_level(LEVEL_MAP)

# --- GAME LOOP ---
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and player.sprite.alive:
                player.sprite.jump()
            # Reset game
            if event.key == pygame.K_r and not player.sprite.alive:
                # Xóa hết đi vẽ lại từ đầu
                player.empty()
                enemies_group.empty()
                tile_group.empty()
                item_group.empty()
                setup_level(LEVEL_MAP)

    # 1. UPDATE
    # Lưu ý: truyền tile_group vào update của player để check va chạm
    player.sprite.update(projectile_group, tile_group) 
    
    enemies_group.update()
    projectile_group.update()
    item_group.update()
    # (Tile không cần update vì nó đứng yên, trừ khi làm camera)

    # 2. COLLISION (Logic cũ)
    # Kiếm vs Quái
    sword_rect = player.sprite.get_sword_rect()
    if sword_rect:
        for enemy in enemies_group:
            if sword_rect.colliderect(enemy.rect): enemy.kill()

    # Phi tiêu vs Quái
    pygame.sprite.groupcollide(projectile_group, enemies_group, True, True)
    
    # Phi tiêu vs Tường (Đạn bắn vào tường thì mất)
    pygame.sprite.groupcollide(projectile_group, tile_group, True, False)

    # Nhặt đồ
    picked_items = pygame.sprite.spritecollide(player.sprite, item_group, True)
    for item in picked_items:
        if item.item_type == 'ammo': player.sprite.ammo += AMMO_PICKUP_AMOUNT
        elif item.item_type == 'health': player.sprite.start_healing(HEALTH_PICKUP_AMOUNT)
        elif item.item_type == 'coin': player.sprite.gold += 10

    # Bị quái đánh
    if pygame.sprite.spritecollide(player.sprite, enemies_group, False):
        player.sprite.take_damage(20)

    # 3. DRAW
    screen.fill(SKY_BLUE)
    
    tile_group.draw(screen) # Vẽ đất
    item_group.draw(screen)
    enemies_group.draw(screen)
    player.sprite.draw(screen)
    projectile_group.draw(screen)

    # UI
    # Thanh máu
    pygame.draw.rect(screen, RED, (20, 20, 200, 20))
    current_hp = int((player.sprite.hp / player.sprite.max_hp) * 200)
    pygame.draw.rect(screen, GREEN, (20, 20, current_hp, 20))
    pygame.draw.rect(screen, (255,255,255), (20, 20, 200, 20), 2)
    
    # Text
    ammo_text = font.render(f"Ammo: {player.sprite.ammo}", True, (255, 255, 255))
    screen.blit(ammo_text, (20, 50))

    if not player.sprite.alive:
        msg = font.render("GAME OVER - Press R", True, RED)
        screen.blit(msg, (SCREEN_WIDTH/2 - 100, SCREEN_HEIGHT/2))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
git add .