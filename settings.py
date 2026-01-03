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
GATE_WIDTH = TILE_SIZE * 1.8
GATE_HEIGHT = TILE_SIZE * 2.6
 
REQUIRED_KEYS = 3 

#X: Đất F: Cổng kết thúc P: Người chơi W: Sói D: Hiệp sĩ bóng tối L: Trùm lửa K: Chìa khóa H: Bình máu A: Đạn (Ammo)

LEVEL_0 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                    K                                                             X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                               XX         XX                                                      X',
'X                              XX         XX                                                       X',
'X                             XX           XX                       K              W               X',
'X            XXXXX           XX        H    XX                    XXXXX          XXXXX   XXXXX     X',
'X           X               XX       XXX      XX                XX     XX      XX     XXX          X',
'X           X              XX                  XX             XX         XXXXXX                   XX',
'X P         X K       W   XX       W             XX  W      XX            XXXX                  F XX',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_1 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X                                                                                                  X',
'X                                                                                                  X',
'X             K                                                                                    X',
'X           XXXXX                                    K                                             X',
'X                                                  XXXXX                          K                X',
'X                                                                      L  x     XXXXX      X       X',
'X                                  H          W              A       XXXXXX                X F     X',
'X P                   XXXXX      XXXXX      XXXXX          XXXXX                           XXXXX   X',
'XXXXX     XX   X                                                                                XX X',
'X         X     X                                                                                  X',
'X         X     XXX                                                                                X',
'X      L  X     X    W                         W                    W                              X',
'XXXXXXXXXXX     XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
]

LEVEL_2 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X  P                                                   K                                         F X',
'XXXXXXXXXXXXX                              W         XXXXX                XXXXX                XXXXX',
'X           X                            XXXXX     XX     XX            XX     XX            XX    X',
'X      K    X             H            XX     XXXXX         XX        XX         XX   D    XX      X',
'X           X            XXXXX       XX                                            XX    XX        X',
'X           X          XX     XX   XX                                                XXXX          X',
'X        W  X       XXX         XXX            H             K             A                       X',
'X       XXXXX     XX                         XXXXX         XXXXX         XXXXX                     X',
'X      XX   X    X                                                                                 X',
'X    XX     X   XXX                                  XXX                                XXXXX      X',
'X                                                                                       X          X',
'X                          W                                      L                     X       D  X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX     XXXXXX',
]

LEVEL_3 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X   P                         H                             A              K                     F X',
'X            XXXXX          XXXXX          XXXXX          XXXXX          XXXXX                 XXXXX',
'X          XX     XX      XX     XX      XX     XX      XX     XX      XX     XX             XX    X',
'XXXXXXXXXXX                        XXXXXX                        XXXXXX         XXXXXX     XX      X',
'X                                                                                                  X',
'X                                                    XXX                                           X',
'X   K W           H                 W                             W              D                 X',
'X  XXXXXXX        XXXXXXX        XXXXXXX          K            XXXXXXX        XXXXXXX              X',
'X                                                XXX                                               X',
'X                                                                                                  X',
'X                                                                                                  X',
'X                           X    X                       X    X                                    X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXXXXXXXX     XXXXXXXXX',
]

LEVEL_4 = [
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
'X                                                                                                  X',
'X      K                                                                                           X',
'X                                                                                                F X',
'X              L                             K               D            K            XXXXX   XXXXX',
'X             XXXXX           W             XXXXX           XXXXX        XXXXX        XX   XX XX   X',
'X                           XXXXX                         XX     XX    XX     XX      X     XXX   KX',
'X                         XX     XX                     XX         XXXX        XX                  X',
'X P  XXXX               XX         XX                 XX                         XXX               X',
'XXXXX    XX           XX             XX             XX       H                      XX             X',
'X          XX       XX       H         XX         XX                 A                XX           X',
'X            XXXXXXX                     XXX   XXX                                      XXXXXX     X',
'X      K                                                                                           X',
'X D                  D          W                            L                                     X',
'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX    XXXXXXXXXXXXXXXXXX',
]

ALL_LEVELS = [LEVEL_0, LEVEL_1, LEVEL_2, LEVEL_3, LEVEL_4]