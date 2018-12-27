#Modules
import pygame
import random
from random import randint
import time
import sys

# Variables CHANGE IF NEEDED
WHITE = (255,255,255)
BLACK = (0,0,0)
WIDTH = 800
HEIGHT = 600
TITLE = 'PONG'
FPS = 30
gamestate = 0

#Window Class
class Window:
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.surface = pygame.display.set_mode((self.width,self.height)) #!!!

class Ball(pygame.sprite.Sprite):

    def __init__ (self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed = [randint(5,10), randint(5,10)]

    def update(self):
        if self.rect.y > (HEIGHT-10) or self.rect.y < 0:
            self.speed[1] *= -1
            if gamestate == 1:
                hitwall.play()

        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def reset(self,serve_to):
        self.serve_to = serve_to
        self.rect.center = (WIDTH / 2, HEIGHT / 2)
        self.speed = [randint(5,10), randint(5,10)]
        if self.serve_to == 'left':
            self.speed[0] *= -1
        if randint(0,2) == 0:
            self.speed[1] *= -1

#Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self,x_cood,y_cood):
        pygame.sprite.Sprite.__init__(self)
        self.x_cood = x_cood
        self.y_cood = y_cood
        self.image = pygame.Surface((10, 50))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x_cood,self.y_cood)
        self.move = 'no'

    #MOVEMENT, EDIT IF NEcESSARY
    def update(self):
        if self.move == 'up' and self.rect.y >= 0:
            self.rect.y -= 20
        elif self.move == 'down'and self.rect.y <= 550:
            self.rect.y += 20

    def reset(self):
        self.rect.y = HEIGHT/2


#Initialise modules and screen and clock
pygame.init()
pygame.mixer.init()
pygame.font.init()


screen = Window(WIDTH,HEIGHT)
screen.surface.fill(BLACK)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

#Sprite group and objects
all_sprites = pygame.sprite.Group()
player1 = Player(40,300)
player2 = Player(750,300)
ball = Ball()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

font = pygame.font.Font("PressStart2P.ttf", 72)
caption_font = pygame.font.Font("PressStart2P.ttf", 16)
score1 = 0
score2 = 0

frames = 0

hitwall = pygame.mixer.Sound('ping_pong_8bit_beeep.wav')
hitbat = pygame.mixer.Sound('ping_pong_8bit_plop.wav')
scorepoint = pygame.mixer.Sound('ping_pong_8bit_peeeeeep.wav')

gameisrunning = True
go = 'yes'

#MAIN GAME LOOP
while gameisrunning == True:
    clock.tick(FPS)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player2.move = 'up'
            elif event.key == pygame.K_DOWN:
                player2.move = 'down'
            elif event.key == pygame.K_w:
                player1.move = 'up'
            elif event.key == pygame.K_s:
                player1.move = 'down'
            elif event.key == pygame.K_RETURN:
                if gamestate == 0:
                    gamestate = 1
                    ball.reset('left')
                    pygame.time.delay(1000)


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player2.move = 'no'
            elif event.key == pygame.K_DOWN:
                player2.move = 'no'
            elif event.key == pygame.K_w:
                player1.move = 'no'
            elif event.key == pygame.K_s:
                player1.move = 'no'

    if gamestate == 0:
        if ball.rect.x > WIDTH:
            ball.rect.x = WIDTH
            ball.speed[0] *= -1

        if ball.rect.x < 0:
            ball.rect.x = 0
            ball.speed[0] *= -1

        caption_timer = pygame.time.get_ticks()

        if (caption_timer % 1000) <= 500:
            caption = caption_font.render("Press Enter to Start", False, (255, 255, 255))
            screen.surface.blit(caption, (240,480))

    if gamestate == 1:

        if pygame.sprite.collide_rect(player1, ball):
            hitbat.play()
            ball.speed[0] = round(ball.speed[0] * -1.1)
            ball.speed[1] = round(ball.speed[0] * 1.1)
            ball.rect.x = 40

        if pygame.sprite.collide_rect(player2, ball):
            hitbat.play()
            ball.speed[0] = round(ball.speed[0] * -1.1)
            ball.speed[1] = round(ball.speed[1] * 1.1)
            ball.rect.x = 730

        if ball.rect.x > WIDTH:
            scorepoint.play()
            score1 += 1
            initialticks = pygame.time.get_ticks()
            while pygame.time.get_ticks()-initialticks < 2000:
                go = 'no'
            ball.reset('left')

        if ball.rect.x < 0:
            scorepoint.play()
            score2 += 1
            initialticks = pygame.time.get_ticks()
            while pygame.time.get_ticks()-initialticks < 2000:
                go = 'no'
            ball.reset('right')

        if score1 > 10 or score2 > 10:
            pygame.time.delay(2000)
            gamestate = 0

        scoreboard1 = font.render(str(score1), False, (255, 255, 255))
        scoreboard2 = font.render(str(score2), False, (255, 255, 255))
        screen.surface.blit(scoreboard1, (250,60))
        screen.surface.blit(scoreboard2, (480,60))

    for i in range(0,40):
        pygame.draw.rect(screen.surface,(255,255,255),(WIDTH/2,20*i,2,10))


    all_sprites.update()
    all_sprites.draw(screen.surface)

    pygame.display.flip()
    screen.surface.fill(BLACK)
