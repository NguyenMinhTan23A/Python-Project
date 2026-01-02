# settings.py

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 720
FPS = 60

# Vật lý
GRAVITY = 0.8
JUMP_FORCE = -16
MOVE_SPEED = 5
MAX_JUMPS = 2

# Kích thước
KNIGHT_SIZE = (70, 70)
DRAW_OFFSET_Y = 0

# Màu sắc
SKY_BLUE = (135, 206, 235)
GREEN = (34, 139, 34)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
GRAY = (100, 100, 100) 

# Cấu hình Game
START_AMMO = 5
AMMO_PICKUP_AMOUNT = 3
PROJECTILE_SPEED = 15
PROJECTILE_SIZE = (30, 30)
DASH_SPEED = 10      
DASH_DURATION = 25   
DASH_COOLDOWN = 60   
HEALTH_PICKUP_AMOUNT = 30
TILE_SIZE = 50
GATE_WIDTH = TILE_SIZE * 1.5
GATE_HEIGHT = TILE_SIZE * 2.3
 
REQUIRED_KEYS = 3 

# --- HỆ THỐNG LEVEL (ĐÃ SỬA LẠI LOGIC: DỄ LẤY CHÌA HƠN) ---
# Quy tắc: 1 dòng trần, 1 dòng sàn.
# Chìa khóa (K) được đặt trên bục hoặc độ cao vừa phải.

# LEVEL 1: ĐỒNG CỎ (Khởi động nhẹ nhàng)
LEVEL_0 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                     K                                                            X',
'X                                   XXXXX                                                          X',
'X                 K               XX     XX                         K              E       F       X',
'X P             XXXXX           XX         XX                     XXXXX          XXXXX   XXXXX     X',
'XXXX          XX     XX       XX             XX                 XX     XX      XX     XXX     XX   X',
'X           XX         XX   XX                 XX             XX         XX  XX                 XX X',
'X      E  XX             XXX                     XX  E      XX             XXX                    XX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

# LEVEL 2: KHÔNG GIAN (Nhảy qua các bục bay)
LEVEL_1 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X             K                                                                                    X',
'X           XXXXX                                    K                                             X',
'X                                                  XXXXX                          K                X',
'X                                                                               XXXXX              X',
'X                       E          H          E              A          E                    F     X',
'X P                   XXXXX      XXXXX      XXXXX          XXXXX      XXXXX                XXXXX   X',
'XXXX       XXXXX     XX   XX    XX   XX    XX   XX        XX   XX    XX   XX             XX     XX X',
'X         XX   XX                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

# LEVEL 3: LEO NÚI (Chìa khóa ở trên đỉnh)
LEVEL_2 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X                                                      K                    E                    F X',
'X                                          E         XXXXX                XXXXX                XXXXX',
'X                                        XXXXX     XX     XX            XX     XX            XX    X',
'X                          K           XX     XX XX         XX        XX         XX        XX      X',
'X                        XXXXX       XX                                            XX    XX        X',
'X                      XX     XX   XX                                                XXXX          X',
'X          E         XX         XXX            H             K             A                       X',
'X P      XXXXX     XX                        XXXXX         XXXXX         XXXXX                     X',
'XXXX   XX     XX XX                                                                                X',
'X    XX                                                                                            X',
'X                                                                                                  X',
'X                                                                                                  X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

# LEVEL 4: HẦM MỘ (Trần thấp, Chìa khóa giấu trong hốc)
LEVEL_3 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X   P          K              H              K              A              K                     F X',
'X            XXXXX          XXXXX          XXXXX          XXXXX          XXXXX                 XXXXX',
'X          XX     XX      XX     XX      XX     XX      XX     XX      XX     XX             XX    X',
'XXXXXXXXXXX         XXXXXX         XXXXXX         XXXXXX         XXXXXX         XXXXXX     XX      X',
'X                                                                                                  X',
'X                                                                                                  X',
'X     E              E              E              E              E              E                 X',
'X  XXXXXXX        XXXXXXX        XXXXXXX        XXXXXXX        XXXXXXX        XXXXXXX              X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

# LEVEL 5: HỖN HỢP (Khó nhất - Vực sâu)
LEVEL_4 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                        E       F X',
'X               K                             K               E            K           XXXXX   XXXXX',
'X             XXXXX           E             XXXXX           XXXXX        XXXXX        XX   XX XX   X',
'X                           XXXXX                         XX     XX    XX     XX     XX     XXX    X',
'X     E                   XX     XX                     XX         XXXX         XX                 X',
'X P XXXXX               XX         XX                 XX                          XX               X',
'XXXX     XX           XX             XX             XX                              XX             X',
'X          XX       XX                 XX         XX                                  XX           X',
'X            XXXXXXX                     XXXXXXXXX                                      XXXXXXXX   X',
'X                                                                                                  X',
'X                                                                                                  X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

ALL_LEVELS = [LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4]