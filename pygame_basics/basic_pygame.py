import pygame
import os
import random as rnd
import time
pygame.init()

WINDOW_W = 700
WINDOW_H = 400
# Maximun number of pixels that the character is going to jump
JUMP_MAX = 10
# Margin to get Actual box for collition (The higher the margin the less probably is going to collapse)
MRG_X = 20
MRG_Y = 20
# MAXIMUM NUMBER OF COLLITIONS
MAX_LIFES = 3
# MAX NUMBER OF BULLETS IN SCREEN
MAX_BULLETS = 5

increment_speed_enemies = 1.2
frequency_send_enemies = 1 # Entre mas baja envia con mas frecuencia
lives = MAX_LIFES
score = 0
num_enemies_start = 3
recovery_mode = 0
game_is_over = False
last_shot     = 0
shot_interval = 500 # In milliseconds

clock = pygame.time.Clock()
font = pygame.font.SysFont('verdana', 15, True)

# LOAD THE IMAGES 
cur_path = os.getcwd() + '\pygame_basics\GameImgs'
walkRight = [pygame.image.load(cur_path + '\R1.png'), pygame.image.load(cur_path + '\R2.png'), pygame.image.load(cur_path + '\R3.png'), 
             pygame.image.load(cur_path + '\R4.png'), pygame.image.load(cur_path + '\R5.png'), pygame.image.load(cur_path + '\R6.png'), pygame.image.load(cur_path + '\R7.png'), pygame.image.load(cur_path + '\R8.png'), pygame.image.load(cur_path + '\R9.png')]
walkLeft  = [pygame.image.load(cur_path + '\L1.png'), pygame.image.load(cur_path + '\L2.png'), pygame.image.load(cur_path + '\L3.png'), 
             pygame.image.load(cur_path + '\L4.png'), pygame.image.load(cur_path + '\L5.png'), pygame.image.load(cur_path + '\L6.png'), pygame.image.load(cur_path + '\L7.png'), pygame.image.load(cur_path + '\L8.png'), pygame.image.load(cur_path + '\L9.png')]
walkRight_En = [pygame.image.load(cur_path + '\R1E.png'), pygame.image.load(cur_path + '\R2E.png'), pygame.image.load(cur_path + '\R3E.png'), 
             pygame.image.load(cur_path + '\R4E.png'), pygame.image.load(cur_path + '\R5E.png'), pygame.image.load(cur_path + '\R6E.png'), pygame.image.load(cur_path + '\R7E.png'), pygame.image.load(cur_path + '\R8E.png'), pygame.image.load(cur_path + '\R9E.png'),
             pygame.image.load(cur_path + '\R10E.png'), pygame.image.load(cur_path + '\R11E.png')]
walkLeft_En  = [pygame.image.load(cur_path + '\L1E.png'), pygame.image.load(cur_path + '\L2E.png'), pygame.image.load(cur_path + '\L3E.png'), 
             pygame.image.load(cur_path + '\L4E.png'), pygame.image.load(cur_path + '\L5E.png'), pygame.image.load(cur_path + '\L6E.png'), pygame.image.load(cur_path + '\L7E.png'), pygame.image.load(cur_path + '\L8E.png'), pygame.image.load(cur_path + '\L9E.png'),
             pygame.image.load(cur_path + '\L10E.png'), pygame.image.load(cur_path + '\L11E.png'),]
bg   = pygame.image.load(cur_path + '\sbg.png')
game_over = pygame.image.load(cur_path + '\game_over.jpg')
char = pygame.image.load(cur_path + '\standing.png')

# LOAD THE MUSIC AND EFFECTS
jump_snd = pygame.mixer.Sound(cur_path + '\jump.wav')
gunshot_snd = pygame.mixer.Sound(cur_path + '\shot2.wav')
loselive_snd = pygame.mixer.Sound(cur_path + '\lose_live.wav')
gameover_snd = pygame.mixer.Sound(cur_path + '\game_over.wav')
bg_music = pygame.mixer.music.load(cur_path + '\music.mp3')
#pygame.mixer.music.play(-1)

win = pygame.display.set_mode((WINDOW_W, WINDOW_H))
pygame.display.set_caption("My First Game V.1.0")

class enemy():
    def __init__(self, x, y, w, h, vel = 7):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.left  = True
        self.right = False
        self.velocity = vel
        self.walkCount = 0

    def draw(self, win):
        # 27 / 2.45 = 11 
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if self.left:
            win.blit(walkLeft_En[int(self.walkCount/2.4545)], (self.x, self.y))
            self.walkCount += 1
        elif self.right:
            win.blit(walkRight_En[int(self.walkCount/2.4545)], (self.x, self.y))
            self.walkCount += 1
        else:
            win.blit(walkLeft_En[0], (self.x, self.y))
            self.walkCount = 0

        #pygame.draw.rect(win, (100,255,100), (self.x, self.y, self.w, self.h), 2)
        #pygame.draw.rect(win, (200,255,200), (self.x + MRG_X, self.y + MRG_Y , self.w - 2*MRG_X, self.h - 2*MRG_Y), 1)

    def move(self):
        if self.left and self.x <= rnd.randint(self.w, 100):
            self.left  = False
            self.right = True

        if self.right and self.x >=  (WINDOW_W - rnd.randint(self.w, 100)):
            self.left  = True
            self.right = False

        if self.left:
            self.x -= self.velocity
        elif self.right:
            self.x += self.velocity

class player():
    def __init__(self, x, y, w, h, vel = 7):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.velocity = vel
        self.isJumping = False
        self.left  = False
        self.right = False
        self.walkCount = 0
        self.jumpCount = JUMP_MAX
        self.standing = True

    def draw(self, win):
        # Because there are 9 images for each left, right. And we want each image to appear for 3 frames. 
        # and we want a total frames for each cycle of 27 steps. Then we need 27 / 3 = 9 images per cycle
        if self.walkCount + 1 >= 27:
            self.walkCount = 0

        if not self.standing:
            if self.left:
                # Show each image 3 times every animation
                win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
            elif person.right:
                win.blit(walkRight[self.walkCount//3], (self.x,self.y))
                self.walkCount += 1
        else:
            if self.left:
                win.blit(walkLeft[0], (self.x,self.y))
            else:
                win.blit(walkRight[0], (self.x,self.y))
            
            #win.blit(char, (self.x,self.y))
            self.swalkCount = 0

        #pygame.draw.rect(win, (255,100,100), (self.x, self.y, self.w, self.h), 2)
        #pygame.draw.rect(win, (255,200,200), (self.x + MRG_X, self.y + MRG_Y , self.w - 2*MRG_X, self.h - 2*MRG_Y), 1)

    def collide(self, e):
        it_collide = False
        if ((self.x + MRG_X >= e.x + MRG_X) and (self.x + MRG_X <= (e.x + e.w - MRG_X))) or (((self.x + self.w - MRG_X) >= e.x + MRG_X) and ((self.x + self.w - MRG_X) <= (e.x + e.w - MRG_X))):
            if ((self.y + MRG_Y >= e.y + MRG_Y) and (self.y + MRG_Y <= (e.y + e.h - MRG_Y))) or (((self.y + self.h - MRG_Y) >= e.y + MRG_Y) and ((self.y + self.h - MRG_Y) <= (e.y + e.h - MRG_Y))):
                it_collide = True

        return it_collide

class bullet():
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y 
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 8 * direction
        self.w = self.radius*2
        self.h = self.radius*2

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)
        pygame.draw.rect(win, (200,200,255), (self.x - self.radius, self.y - self.radius, self.w, self.h), 1)

    def collide(self, e):
        it_collide = False
        if ((self.x >= e.x + MRG_X) and (self.x <= (e.x + e.w - MRG_X))) or (((self.x + self.w) >= e.x + MRG_X) and ((self.x + self.w) <= (e.x + e.w - MRG_X))):
            if ((self.y >= e.y) and (self.y <= (e.y + e.h))) or (((self.y + self.h) >= e.y) and ((self.y + self.h) <= (e.y + e.h))):
                it_collide = True

        return it_collide


def InitializeGame():
    global game_is_over, recovery_mode, frequency_send_enemies, increment_speed_enemies

    game_is_over            = False
    recovery_mode           = 0
    frequency_send_enemies  = 1
    increment_speed_enemies = 1.2

    # Initialize the player
    person = player(10, 220, 64, 64)

    # Initialize the enemies
    enemies = []
    for i in range(num_enemies_start):
        start_point_x = rnd.randint(50, WINDOW_W - 50)
        enemies.append(enemy(start_point_x, 225, 64, 64, 3))

    return person, enemies

# Function that re draw all our scenario
def redrawGameWindow():
    global game_is_over

    # Reset background
    win.blit(bg, (0,0))
    # Draw the person
    person.draw(win)
    # Draw the enemy
    for enemy_k in enemies:
        enemy_k.draw(win)
    # Draw the bullets 
    for bull in bullets:
        bull.draw(win)
    # Text Lives
    text = font.render("LIVES: " + str(lives), 1, (255,255,255))
    win.blit(text, (WINDOW_W - 120, 10))
    # Text Score
    text = font.render("SCORE: " + str(score), 1, (255,255,255))
    win.blit(text, (40, 10))

    # If Game is Over
    if lives <= 0:
        if not game_is_over:
            gameover_snd.play()
            game_is_over = True
        win.fill((0,0,0))
        win.blit(game_over, (0,0))
        pygame.mixer.music.stop()
        pygame.display.update()

    pygame.display.update()


person, enemies = InitializeGame()

bullets = []

# Function that gets the current time in milliseconds
getCurrentMillis = lambda: int(round(time.time() * 1000))

run = True
while run:
    # Number of images per second
    clock.tick(27)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

    for bull in bullets:
        if bull.x < WINDOW_W and bull.x > 0:
            bull.x += bull.velocity
        else:
            bullets.pop(bullets.index(bull))

    keys = pygame.key.get_pressed()

    # CHECK IF THERE ARE NOT MORE ENEMIES AND SEND MORE
    if len(enemies) == 0:
        # Increment speed
        increment_speed_enemies += 0.05
        # Aumentar la frecuencia con la que se envian enemigos
        frequency_send_enemies = 0.999 * frequency_send_enemies
        print(f"Increment in level => Frequencia de envio: {(1-frequency_send_enemies)}")
        enemies.append(enemy(WINDOW_W + rnd.randint(0,30), 225, 64, 64, 3+increment_speed_enemies))

    # FREQUENCY OF SENDING ENEMIES 
    if rnd.random() <= (1-frequency_send_enemies):
        enemies.append(enemy(WINDOW_W + rnd.randint(0,30), 225, 64, 64, 3))

    # CHECK IF BULLET COLLIDE
    for bull in bullets:
        for enemy_k in enemies:
            if bull.collide(enemy_k):
                score += 1
                try:
                    bullets.pop(bullets.index(bull))
                    enemies.pop(enemies.index(enemy_k))
                except:
                    pass

    # CHECK IF THE PLAYER COLLIDE WITH ENEMY
    if recovery_mode > 0:
        recovery_mode -= 1

    for enemy_k in enemies:
        if person.collide(enemy_k) and recovery_mode == 0:
            if not game_is_over and lives > 1:
                loselive_snd.play()
            lives -= 1
            recovery_mode = 10

    # SHOOT 
    if keys[pygame.K_SPACE]:
        facing = 1
        if person.left:
            facing = -1
        elif person.right:
            facing = 1

        if len(bullets) < MAX_BULLETS and (getCurrentMillis() > last_shot + shot_interval):
            gunshot_snd.play()
            last_shot = getCurrentMillis()
            bullets.append(bullet(round(person.x + person.w/2), round(person.y + person.h/2), 6, (0,0,0), facing))
    

    # IF RESTART GAME 
    if keys[pygame.K_r]:
        lives = MAX_LIFES
        score = 0
        person, enemies = InitializeGame()

    # MOVE THE ENEMY
    # If the enemy reached a specific point in the screen then change direction
    for enemy_k in enemies:
        enemy_k.move()

    # MOVING THE PLAYER
    if keys[pygame.K_LEFT] and person.x > 0:
        person.x -= person.velocity
        person.left  = True
        person.right = False
        person.standing = False
    elif keys[pygame.K_RIGHT] and person.x < (WINDOW_W - person.w):
        person.x += person.velocity
        person.left  = False
        person.right = True
        person.standing = False
    else:
        person.standing = True
        person.walkCount = 0

    # EVENTS WHEN IS JUMPING OR NOT
    if not person.isJumping:
        if keys[pygame.K_UP]:
            jump_snd.play()
            person.isJumping = True
            person.left      = False
            person.right     = False
            person.walkCount = 0 
    else:
        if person.jumpCount >= (-1 * JUMP_MAX):
            neg = -1 if person.jumpCount < 0 else 1
            #y -= (person.jumpCount ** 2) * 0.25 * neg
            person.y -= (person.jumpCount * abs(person.jumpCount)) * 0.5
            person.jumpCount -= 1
        else:
            person.isJumping = False
            person.jumpCount = JUMP_MAX

    redrawGameWindow()
