import pygame
import random
import math

from pygame import mixer

#initialize the pygame
pygame.init()

#create the screen
screen = pygame.display.set_mode((800,599))

#background
background = pygame.image.load(r'C:\Users\ASUS\pythonproject\.vscode\WhatsApp Image 2020-12-22 at 21.33.04.jpeg')

#backgroung music
mixer.music.load(r'C:\Users\ASUS\pythonproject\.vscode\background.wav')
mixer.music.play(-1)

#display
pygame.display.set_caption("Space Fighters")
icon = pygame.image.load(r'C:\Users\ASUS\pythonproject\.vscode\project.png')
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load(r'C:\Users\ASUS\pythonproject\.vscode\spaceship (1).png')
playerX = 370
playerY = 480
playerX_change = 0

#enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r'C:\Users\ASUS\pythonproject\.vscode\asteroid.png'))
    enemyX.append(random.randint(0,735))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(0.3)
    enemyY_change.append(40) 

#bullet
#ready : u cant see the bullet
#fire : u can see the bullet
bulletImg = pygame.image.load(r'C:\Users\ASUS\pythonproject\.vscode\bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1 
bullet_state = "ready" 

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',32)

textX = 10
textY = 10

#game over text
over_font = pygame.font.Font('freesansbold.ttf',64)


def show_score(x,y):
    score = font.render("Score : "+ str(score_value),True, (255,255,255))
    screen.blit(score,(x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255,255,255))
    screen.blit(over_text,(200,250))

def player(playerX,playerY):
    screen.blit(playerImg,(playerX,playerY))

def enemy(enemyX,enemyY,i):
    screen.blit(enemyImg[i],(enemyX,enemyY))

def fire_bullet(bulletX,bulletY):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg,(bulletX + 16,bulletY + 10))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX-bulletX,2) + math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else: 
        return False
#game loop
running = True
while running:
    screen.fill((0,0,0))
    #background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #keystroke is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.3
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound(r'C:\Users\ASUS\pythonproject\.vscode\laser.wav')
                    bullet_sound.play()
                #get the current coordinates of the spaceship 
                    bulletX = playerX
                    fire_bullet(bulletX,bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
#checking for boundary of spaceship
    if playerX <= 0:
        playerX = 0 
    elif playerX >= 736:
        playerX = 736

#bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"
         

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change

#checking for boundary of enemy
    for i in range(num_of_enemies):
        #game over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3 
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]
 
        #collision
        Collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
        if Collision:
            explosion_sound = mixer.Sound(r'C:\Users\ASUS\pythonproject\.vscode\explosion.wav')
            explosion_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            print(score_value)
            enemyX[i] = random.randint(0,735)
            enemyY[i] = random.randint(50,150)
        
        enemy(enemyX[i],enemyY[i],i)

 
 
 
 
 
 
 
    player(playerX,playerY)
    show_score(textX,textY)
    pygame.display.update()