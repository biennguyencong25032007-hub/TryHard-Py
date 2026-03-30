import pygame, random, sys, os, math

pygame.init()

try:
    pygame.mixer.init()
    SOUND = True
except:
    SOUND = False

WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

BLACK = (15, 15, 15)
GREEN_HEAD = (0, 255, 180)
GREEN_BODY = (0, 200, 120)
RED = (255, 80, 80)
WHITE = (255, 255, 255)

font_big = pygame.font.SysFont("Arial", 50)
font = pygame.font.SysFont("Arial", 28)

def play_sound(freq=500, duration=0.1):
    if not SOUND:
        return
    sample_rate = 44100
    n_samples = int(sample_rate * duration)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        val = int(32767 * math.sin(2 * math.pi * freq * t))
        buf += val.to_bytes(2, byteorder="little", signed=True)
    pygame.mixer.Sound(buffer=bytes(buf)).play()

def load_highscore():
    if os.path.exists("highscore.txt"):
        return int(open("highscore.txt").read())
    return 0

def save_highscore(s):
    open("highscore.txt", "w").write(str(s))

def spawn_food():
    return (
        random.randint(0, (WIDTH - CELL)//CELL) * CELL,
        random.randint(0, (HEIGHT - CELL)//CELL) * CELL
    )

def reset_game():
    return [(100,100)], (CELL,0), spawn_food(), 0

state = "menu"
snake, direction, food, score = reset_game()
high = load_highscore()

while True:
    clock.tick(FPS)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if state == "menu":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    snake, direction, food, score = reset_game()
                    state = "game"

        elif state == "game":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP and direction != (0, CELL):
                    direction = (0, -CELL)
                if e.key == pygame.K_DOWN and direction != (0, -CELL):
                    direction = (0, CELL)
                if e.key == pygame.K_LEFT and direction != (CELL, 0):
                    direction = (-CELL, 0)
                if e.key == pygame.K_RIGHT and direction != (-CELL, 0):
                    direction = (CELL, 0)

        elif state == "gameover":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    snake, direction, food, score = reset_game()
                    state = "game"
                if e.key == pygame.K_m:
                    state = "menu"

    screen.fill(BLACK)

    if state == "menu":
        screen.blit(font_big.render("SNAKE", True, GREEN_HEAD), (WIDTH//2 - 100, 200))
        screen.blit(font.render("ENTER: Play", True, WHITE), (WIDTH//2 - 90, 300))

    elif state == "game":
        head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        snake.insert(0, head)

        if head == food:
            score += 1
            play_sound(900, 0.08)
            food = spawn_food()
        else:
            snake.pop()

        if head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or head in snake[1:]:
            play_sound(200, 0.3)
            if score > high:
                save_highscore(score)
                high = score
            state = "gameover"

        for i, s in enumerate(snake):
            color = GREEN_HEAD if i == 0 else GREEN_BODY
            pygame.draw.rect(screen, color, (*s, CELL, CELL), border_radius=6)

        pygame.draw.rect(screen, RED, (*food, CELL, CELL), border_radius=6)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
        screen.blit(font.render(f"High: {high}", True, WHITE), (10, 40))

    elif state == "gameover":
        screen.blit(font_big.render("GAME OVER", True, RED), (WIDTH//2 - 150, 200))
        screen.blit(font.render(f"Score: {score}", True, WHITE), (WIDTH//2 - 80, 270))
        screen.blit(font.render("R: Replay", True, WHITE), (WIDTH//2 - 90, 320))
        screen.blit(font.render("M: Menu", True, WHITE), (WIDTH//2 - 80, 360))

    pygame.display.flip()