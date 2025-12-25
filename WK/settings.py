# settings.py

# Kích thước màn hình
SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
FPS = 60

# Vật lý
GRAVITY = 0.8
JUMP_FORCE = -16
FLOOR_Y = 500  # Vị trí mặt đất
MOVE_SPEED = 5
MAX_JUMPS = 2

# Kích thước nhân vật hiển thị
KNIGHT_SIZE = (70, 70)
DRAW_OFFSET_Y = 0 # Độ lệch để chân chạm đất

# Màu sắc
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GOLD = (255, 215, 0)

# --- CẤU HÌNH TẦM XA ---
START_AMMO = 5
AMMO_PICKUP_AMOUNT = 3
PROJECTILE_SPEED = 15
PROJECTILE_SIZE = (30, 30)
ITEM_COLOR = (0, 0, 255)

# --- CẤU HÌNH LƯỚT (DASH) ---
DASH_SPEED = 10      # Tốc độ lướt (nhanh gấp 3 lần đi bộ)
DASH_DURATION = 25   # Thời gian lướt (10 khung hình ~ 0.15 giây)
DASH_COOLDOWN = 60   # Thời gian hồi chiêu (60 khung hình ~ 1 giây)

# --- CẤU HÌNH HỒI MÁU ---
HEALTH_PICKUP_AMOUNT = 30 

# --- CẤU HÌNH ĐẤT ---
TILE_SIZE = 50
# X: Đất (Tường) P: Vị trí Người chơi E: Quái vật C: Tiền (Coin) H: Máu (Heal) A: Đạn (Ammo)

LEVEL_MAP = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                           XX',
'X    H                      XX',
'X                           XX',
'X                    E      XX',
'X                           XX',
'X                 H         XX',
'X                           XX',
'X         H                 XX',
'X                           XX',
'X P                         XX',
'X        XXX          E     XX',
'XXX                         XX',
'XXX                         XX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]