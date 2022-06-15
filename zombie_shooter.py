import pygame
import random
import math
from pygame import mixer

# initiating pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))

# Design title, Logo
pygame.display.set_caption(" 🤠 Zombie Shooter 🤠 ")
logo = pygame.image.load("logo.png")
pygame.display.set_icon(logo)

# Background image
background = pygame.image.load("military-background2.jpg")

# Background music
mixer.music.load("backg_music.mp3")
mixer.music.play(-1)

# player
playerImg = pygame.image.load("shooter3.png")
playerX = 380
playerY = 510
playerX_change = 0

# Bullet
bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 1.4
bullet_status = "ready"

# Dead line
dead_line = pygame.image.load("line.jpg")
deadlineX = 0
deadlineY = 490

# Score
score = 0
font = pygame.font.Font('bBerlebaranOnline.ttf', 40)
textX = 10
textY = 10

# Game over text
game_over = pygame.font.Font("Black_Ravens.ttf", 90)
final_score = pygame.font.Font("Black_Ravens.ttf", 50)

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
enemy_number = 5


def game_over_text():
    over_text = game_over.render(" GAME OVER ", True, (0, 0, 0))
    score_text2 = final_score.render(" Your final Score : " + str(score), True, (0, 0, 0))
    screen.blit(over_text, (230, 250))
    screen.blit(score_text2, (250, 350))


def show_score(x, y):
    score_text = font.render("Score : " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (x, y))


for i in range(enemy_number):
    enemyImg.append(pygame.image.load("zoombie.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(0, 120))
    enemyX_change.append(.35)
    enemyY_change.append(70)


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def bullet_fire(x, y):
    global bullet_status
    bullet_status = "fire"
    screen.blit(bulletImg, (x + 45, y + 20))


def iscollide(bulletX, bulletY, enemyX, enemyY):
    distance = math.sqrt((math.pow(bulletX - enemyX, 2)) + (math.pow(bulletY - enemyY, 2)))
    if distance < 27:
        return True
    else:
        return False


# quiting the game
running = True
while running:
    # Setting background color .It is in the while loop
    screen.fill((0, 150, 155))
    screen.blit(background, (0, 0))
    screen.blit(dead_line, (deadlineX, deadlineY))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # player control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -.9
            if event.key == pygame.K_RIGHT:
                playerX_change = .9
            if event.key == pygame.K_SPACE:
                if bullet_status is "ready":
                    bulletX = playerX
                    bullet_fire(bulletX, bulletY)
                    # bullet sound
                    bullet_sound = mixer.Sound("bullet.mp3")
                    bullet_sound.play()
        if event.type == pygame.KEYUP:
            playerX_change = 0

    # making boundary and move for player
    playerX += playerX_change
    if playerX < 0:
        playerX = 0
    elif playerX > 736:
        playerX = 736

    # making boundary and move for enemy
    for i in range(enemy_number):

        enemyX[i] += enemyX_change[i]
        if enemyX[i] < 0:
            enemyX_change[i] = .7
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] > 736:
            enemyX_change[i] = -.7
            enemyY[i] += enemyY_change[i]

        # collision here
        collision = iscollide(bulletX, bulletY, enemyX[i], enemyY[i])
        if collision:
            bulletY = 480
            bullet_status = "ready"
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(0, 120)
            score += 5
            collision_sound = mixer.Sound("scream.mp3")
            collision_sound.play()
        enemy(enemyX[i], enemyY[i], i)

        # Game Over

        if enemyY[i] > 450:
            for j in range(5):
                enemyY[j] = 1000
            game_over_text()

        # bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_status = "ready"

    if bullet_status is "fire":
        bullet_fire(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
