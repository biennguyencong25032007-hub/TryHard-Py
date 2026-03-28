import pygame, random, math, sys, os

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("SPACE SHOOTER STABLE")

clock = pygame.time.Clock()

WHITE=(255,255,255)
RED=(255,0,0)
GREEN=(0,255,0)
YELLOW=(255,255,0)
BLUE=(0,150,255)
BLACK=(0,0,0)

font = pygame.font.SysFont("Arial", 22)
big_font = pygame.font.SysFont("Arial", 50)

# Highscore
if not os.path.exists("highscore.txt"):
    open("highscore.txt","w").write("0")

def get_highscore():
    return int(open("highscore.txt").read())

def save_highscore(s):
    if s > get_highscore():
        open("highscore.txt","w").write(str(s))

# Player
class Player:
    def __init__(self):
        self.x = WIDTH//2
        self.y = HEIGHT-80
        self.speed = 6
        self.hp = 5
        self.cooldown = 0
        self.power = 1

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x>0: self.x-=self.speed
        if keys[pygame.K_RIGHT] and self.x<WIDTH-50: self.x+=self.speed

    def shoot(self, bullets):
        if self.cooldown==0:
            for i in range(self.power):
                bullets.append([self.x+25+i*10, self.y])
            self.cooldown = 10

    def update(self):
        if self.cooldown>0: self.cooldown-=1

    def draw(self):
        pygame.draw.polygon(screen, BLUE, [(self.x,self.y),(self.x+25,self.y-40),(self.x+50,self.y)])

# Enemy
class Enemy:
    def __init__(self, level):
        self.x = random.randint(0, WIDTH-40)
        self.y = -40
        self.speed = 2 + level*0.3

    def move(self, player):
        self.y += self.speed
        self.x += math.sin(self.y/30)*3
        if player.x > self.x: self.x += 0.5
        else: self.x -= 0.5

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x,self.y,40,40))

# Boss
class Boss:
    def __init__(self, level):
        self.x = WIDTH//2-60
        self.y = 50
        self.hp = 30 + level*5
        self.bullets = []

    def move(self):
        self.x += math.sin(pygame.time.get_ticks()/400)*3
        if random.randint(0,30)==0:
            self.bullets.append([self.x+50, self.y+60])

    def update(self):
        for b in self.bullets:
            b[1]+=5

    def draw(self):
        pygame.draw.rect(screen, (255,100,100),(self.x,self.y,120,70))
        for b in self.bullets:
            pygame.draw.circle(screen, YELLOW, b, 5)

# Explosion
class Explosion:
    def __init__(self,x,y):
        self.x=x; self.y=y; self.r=1
    def update(self): self.r+=3
    def draw(self):
        pygame.draw.circle(screen, YELLOW,(int(self.x),int(self.y)),self.r)

# PowerUp
class PowerUp:
    def __init__(self):
        self.x=random.randint(0,WIDTH-20)
        self.y=-20
        self.type=random.choice(["heal","power"])
    def move(self): self.y+=3
    def draw(self):
        color = GREEN if self.type=="heal" else BLUE
        pygame.draw.rect(screen,color,(self.x,self.y,20,20))

# Stars
stars = [[random.randint(0,WIDTH), random.randint(0,HEIGHT)] for _ in range(80)]

def draw_stars():
    for s in stars:
        pygame.draw.circle(screen,WHITE,s,1)
        s[1]+=1
        if s[1]>HEIGHT: s[1]=0

# MAIN GAME
def main():
    player = Player()
    enemies=[]
    bullets=[]
    explosions=[]
    powerups=[]
    boss=None

    score=0
    level=1
    frame=0

    running=True
    while running:
        clock.tick(60)
        screen.fill(BLACK)
        draw_stars()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys=pygame.key.get_pressed()
        player.move(keys)
        if keys[pygame.K_SPACE]: player.shoot(bullets)
        player.update()

        frame+=1
        if frame % max(20, 60-level*2)==0:
            enemies.append(Enemy(level))

        if score % 50==0 and score>0 and boss is None:
            boss = Boss(level)

        # bullets
        for b in bullets: b[1]-=8
        bullets=[b for b in bullets if b[1]>0]

        # enemies
        for e in enemies: e.move(player)

        # collision
        for e in enemies[:]:
            for b in bullets[:]:
                if e.x<b[0]<e.x+40 and e.y<b[1]<e.y+40:
                    enemies.remove(e)
                    bullets.remove(b)
                    explosions.append(Explosion(e.x,e.y))
                    score+=1
                    break

        # boss
        if boss:
            boss.move(); boss.update()
            for b in bullets[:]:
                if boss.x<b[0]<boss.x+120 and boss.y<b[1]<boss.y+70:
                    boss.hp-=1
                    bullets.remove(b)
                    if boss.hp<=0:
                        boss=None
                        level+=1
                        score+=30

            for bb in boss.bullets:
                if player.x<bb[0]<player.x+50 and player.y<bb[1]<player.y+40:
                    player.hp-=1

        # powerup
        if random.randint(0,300)==1:
            powerups.append(PowerUp())

        for p in powerups[:]:
            p.move()
            if player.x<p.x<player.x+50 and player.y<p.y<player.y+40:
                if p.type=="heal": player.hp+=1
                else: player.power=min(3, player.power+1)
                powerups.remove(p)

        # enemy hit player
        for e in enemies[:]:
            if player.y<e.y+40:
                enemies.remove(e)
                player.hp-=1

        # explosion
        for ex in explosions[:]:
            ex.update()
            if ex.r>20:
                explosions.remove(ex)

        # draw
        player.draw()
        for b in bullets:
            pygame.draw.rect(screen,YELLOW,(*b,5,10))
        for e in enemies:
            e.draw()
        if boss:
            boss.draw()
        for ex in explosions:
            ex.draw()
        for p in powerups:
            p.draw()

        # UI
        screen.blit(font.render(f"Score: {score}",True,WHITE),(10,10))
        screen.blit(font.render(f"HP: {player.hp}",True,WHITE),(10,35))
        screen.blit(font.render(f"Level: {level}",True,WHITE),(10,60))

        pygame.display.update()

        if player.hp<=0:
            save_highscore(score)
            game_over(score)

# GAME OVER
def game_over(score):
    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("GAME OVER",True,RED),(150,250))
        screen.blit(font.render(f"Score: {score}",True,WHITE),(250,320))
        screen.blit(font.render(f"HighScore: {get_highscore()}",True,WHITE),(230,350))
        screen.blit(font.render("Press R to Restart",True,WHITE),(200,400))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_r:
                    main()

# MENU
def menu():
    while True:
        screen.fill(BLACK)
        screen.blit(big_font.render("SPACE SHOOTER",True,WHITE),(120,250))
        screen.blit(font.render("Press SPACE to Start",True,WHITE),(200,350))
        pygame.display.update()

        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    main()

menu()
