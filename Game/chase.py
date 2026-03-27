import pygame, sys, math, random, time
import urllib.request, io

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 640, 480
TILE = 32
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PACMAN FULL FINAL")
clock = pygame.time.Clock()

def load_img(url, size, color):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = r.read()
        img = pygame.image.load(io.BytesIO(data))
        return pygame.transform.scale(img, size)
    except:
        surf = pygame.Surface(size)
        surf.fill(color)
        return surf

def load_sound(url):
    try:
        with urllib.request.urlopen(url, timeout=5) as r:
            data = r.read()
        return pygame.mixer.Sound(io.BytesIO(data))
    except:
        return None

pacman_open = load_img("https://i.imgur.com/7yUvePI.png",(24,24),(255,255,0))
pacman_close = pygame.Surface((24,24))
pygame.draw.circle(pacman_close,(255,255,0),(12,12),12)

ghost_img = load_img("https://i.imgur.com/QZ6XGQp.png",(24,24),(255,0,0))

eat_sound = load_sound("https://www.soundjay.com/button/beep-07.wav")
power_sound = load_sound("https://www.soundjay.com/button/beep-10.wav")
death_sound = load_sound("https://www.soundjay.com/button/beep-09.wav")

maze = [
"11111111111111111111",
"10000000001100000001",
"10111101101101111001",
"10000001000001000001",
"11110101111101011111",
"10000100010000010001",
"10111111010111111001",
"10000000000000000001",
"11111111111111111111"
]

player = [1,1]
px = player[0]*TILE + TILE//2
py = player[1]*TILE + TILE//2
direction = [0,0]
speed = 2
angle = 0
anim_timer = 0

ghost = [10,5]
gx = ghost[0]*TILE + TILE//2
gy = ghost[1]*TILE + TILE//2

dots = []
for y,row in enumerate(maze):
    for x,col in enumerate(row):
        if col=="0":
            dots.append((x,y))

score = 0
power_mode = False
power_time = 0

def can_move(x,y):
    if y<0 or y>=len(maze) or x<0 or x>=len(maze[0]):
        return False
    return maze[y][x]=="0"

def move_player():
    global px,py,player
    nx = px + direction[0]*speed
    ny = py + direction[1]*speed

    gx_check = int(nx//TILE)
    gy_check = int(ny//TILE)

    if can_move(gx_check, gy_check):
        px = nx
        py = ny
        player = [gx_check, gy_check]

def move_ghost():
    global gx,gy,ghost
    dirs = [[1,0],[-1,0],[0,1],[0,-1]]
    best = None
    best_dist = 9999

    for d in dirs:
        nx = ghost[0] + d[0]
        ny = ghost[1] + d[1]
        if can_move(nx,ny):
            dist = abs(nx-player[0]) + abs(ny-player[1])
            if dist < best_dist:
                best_dist = dist
                best = d

    if best:
        ghost[0] += best[0]
        ghost[1] += best[1]
        gx = ghost[0]*TILE + TILE//2
        gy = ghost[1]*TILE + TILE//2

while True:
    screen.fill((0,0,0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: direction=[-1,0]; angle=180
    if keys[pygame.K_RIGHT]: direction=[1,0]; angle=0
    if keys[pygame.K_UP]: direction=[0,-1]; angle=90
    if keys[pygame.K_DOWN]: direction=[0,1]; angle=-90

    move_player()

    # ghost move chậm
    if pygame.time.get_ticks()%300 < 10:
        move_ghost()

    # animation
    anim_timer += 1
    if anim_timer % 20 < 10:
        pacman_img = pacman_open
    else:
        pacman_img = pacman_close

    pacman_img = pygame.transform.rotate(pacman_img, angle)

    # ăn chấm
    if tuple(player) in dots:
        dots.remove(tuple(player))
        score += 10
        if eat_sound: eat_sound.play()

    # power mode (random trigger)
    if score != 0 and score % 100 == 0:
        power_mode = True
        power_time = time.time()
        if power_sound: power_sound.play()

    if power_mode and time.time() - power_time > 5:
        power_mode = False

    # va chạm
    if player == ghost:
        if death_sound: death_sound.play()
        time.sleep(1)
        print("GAME OVER:",score)
        pygame.quit()
        sys.exit()

    # draw map
    for y,row in enumerate(maze):
        for x,col in enumerate(row):
            if col=="1":
                pygame.draw.rect(screen,(0,0,255),(x*TILE,y*TILE,TILE,TILE),2)

    # dots
    for d in dots:
        pygame.draw.circle(screen,(255,255,255),(d[0]*TILE+16,d[1]*TILE+16),3)

    # player
    screen.blit(pacman_img,(px-12,py-12))

    # ghost
    screen.blit(ghost_img,(gx-12,gy-12))

    # score
    font = pygame.font.SysFont(None,30)
    screen.blit(font.render(f"Score:{score}",True,(255,255,0)),(10,450))

    pygame.display.flip()
    clock.tick(60)
