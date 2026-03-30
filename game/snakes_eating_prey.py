import pygame, random, sys, os, math

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 12

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Evolution")
clock = pygame.time.Clock()

BLACK = (20,20,20)
WHITE = (255,255,255)
RED = (255,80,80)

SKINS = [
    {"name":"Default","head":(0,255,180),"body":(0,200,120),"price":0},
    {"name":"Fire","head":(255,100,0),"body":(255,50,0),"price":20},
    {"name":"Ice","head":(0,200,255),"body":(0,120,255),"price":40},
]

font_big = pygame.font.SysFont("Arial", 50)
font = pygame.font.SysFont("Arial", 25)

def sound(freq):
    sample_rate = 44100
    duration = 0.08
    n = int(sample_rate*duration)
    buf = bytearray()
    for i in range(n):
        val = int(32767*math.sin(2*math.pi*freq*i/sample_rate))
        buf += val.to_bytes(2,"little",signed=True)
    pygame.mixer.Sound(buffer=bytes(buf)).play()

def load_data():
    if os.path.exists("save.txt"):
        return list(map(int, open("save.txt").read().split(",")))
    return [0,0]  # coins, skin

def save_data(coins, skin):
    open("save.txt","w").write(f"{coins},{skin}")

def spawn_food():
    return (random.randint(0,(WIDTH-CELL)//CELL)*CELL,
            random.randint(0,(HEIGHT-CELL)//CELL)*CELL)

def reset():
    return [(100,100)], (CELL,0), spawn_food(), 0

state = "menu"
snake, direction, food, score = reset()

coins, current_skin = load_data()

# BUTTON
def button(text,x,y):
    rect = pygame.Rect(x,y,200,50)
    pygame.draw.rect(screen,(60,60,60),rect,border_radius=8)
    t = font.render(text,True,WHITE)
    screen.blit(t,(x+20,y+10))
    return rect

while True:
    clock.tick(FPS)
    screen.fill(BLACK)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        if e.type == pygame.MOUSEBUTTONDOWN:
            mx,my = pygame.mouse.get_pos()

            if state=="menu":
                if play_btn.collidepoint(mx,my):
                    snake,direction,food,score = reset()
                    state="game"
                if shop_btn.collidepoint(mx,my):
                    state="shop"

            elif state=="shop":
                for i,s in enumerate(SKINS):
                    if skin_btns[i].collidepoint(mx,my):
                        if coins >= s["price"]:
                            coins -= s["price"]
                            current_skin = i
                            save_data(coins,current_skin)

                if back_btn.collidepoint(mx,my):
                    state="menu"

            elif state=="gameover":
                if replay_btn.collidepoint(mx,my):
                    snake,direction,food,score = reset()
                    state="game"
                if menu_btn.collidepoint(mx,my):
                    state="menu"

        if e.type == pygame.KEYDOWN and state=="game":
            if e.key==pygame.K_UP and direction!=(0,CELL):
                direction=(0,-CELL)
            if e.key==pygame.K_DOWN and direction!=(0,-CELL):
                direction=(0,CELL)
            if e.key==pygame.K_LEFT and direction!=(CELL,0):
                direction=(-CELL,0)
            if e.key==pygame.K_RIGHT and direction!=(-CELL,0):
                direction=(CELL,0)

    if state=="menu":
        screen.blit(font_big.render("SNAKE",True,WHITE),(200,150))
        play_btn = button("Play",200,250)
        shop_btn = button("Shop",200,320)

    elif state=="shop":
        screen.blit(font_big.render("SHOP",True,WHITE),(220,100))
        skin_btns=[]
        for i,s in enumerate(SKINS):
            rect = pygame.Rect(150,200+i*80,300,60)
            pygame.draw.rect(screen,(50,50,50),rect,border_radius=10)
            txt = f"{s['name']} - {s['price']}$"
            screen.blit(font.render(txt,True,WHITE),(160,220+i*80))
            skin_btns.append(rect)

        back_btn = button("Back",200,500)
        screen.blit(font.render(f"Coins: {coins}",True,WHITE),(10,10))

    elif state=="game":
        head = (snake[0][0]+direction[0],snake[0][1]+direction[1])
        snake.insert(0,head)

        if head==food:
            score+=1
            coins+=1
            sound(900)
            food=spawn_food()
        else:
            snake.pop()

        if head[0]<0 or head[0]>=WIDTH or head[1]<0 or head[1]>=HEIGHT or head in snake[1:]:
            sound(200)
            save_data(coins,current_skin)
            state="gameover"

        skin = SKINS[current_skin]

        for i,s in enumerate(snake):
            color = skin["head"] if i==0 else skin["body"]
            pygame.draw.rect(screen,color,(*s,CELL,CELL),border_radius=6)

        pygame.draw.rect(screen,RED,(*food,CELL,CELL),border_radius=6)

        screen.blit(font.render(f"Score: {score}",True,WHITE),(10,10))
        screen.blit(font.render(f"Coins: {coins}",True,WHITE),(10,40))

    elif state=="gameover":
        screen.blit(font_big.render("GAME OVER",True,RED),(150,200))
        replay_btn = button("Replay",200,300)
        menu_btn = button("Menu",200,370)

    pygame.display.flip()