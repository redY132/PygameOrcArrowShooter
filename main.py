import pygame
import random
from collections import deque

pygame.init()

SCREEN_WIDTH = 854
SCREEN_HEIGHT = 480

#set frame rate
clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#pygame.display.set_caption()

enemy_image = pygame.image.load('assets/orc.png').convert_alpha()

player_image = pygame.image.load('assets/Soldier-Test.png').convert_alpha()

player_hurt_image = pygame.image.load('assets/soldier-hurt.png').convert_alpha()

bg_image = pygame.image.load('assets/basckgrounds/bg.png').convert_alpha()

arrow_image = pygame.image.load('assets/arrow1.png').convert_alpha()

#addenemy images and animations later
#enemy_image = pygame.image.load()

#VARIABLES
character_size = (30,40)
hitbox_error = -10
character_width = 30 + hitbox_error
character_height = 40 + hitbox_error
character_movement_speed = 4
arrow_size_x = 22
arrow_size_y = 12
enemy_movement_speed = 3
total_arrows = 0
MAX_ENEMIES = 100
hurtFlag = False
hurtFlag_set = pygame.USEREVENT
arrow_count = 1
arrow_bounce = 1
arrow_size = 1
arrow_speed = 1

#COLORS
WHITE = (255,255,255)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, shootingLeft, bounces):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(
            pygame.transform.flip(arrow_image, shootingLeft, False),
            (arrow_size_x * arrow_size, arrow_size_y * arrow_size))
        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        self.rect.x = x
        self.rect.y = y
        self.shootingLeft = shootingLeft
        self.bounces = bounces

    def move(self):
        if(self.shootingLeft):
            self.dx = -4 * arrow_speed 
        else:
            self.dx = 4 * arrow_speed

        if self.rect.x + self.dx < 0:
            self.dx = -self.dx
            self.bounces -= 1
        elif self.rect.right + self.dx > SCREEN_WIDTH:
            self.dx = -self.dx
            self.bounces -= 1
        else:
            self.rect.x += self.dx
        
    def killIfNoMoreBounces(self):
        if self.bounces <= 0:
            self.kill()

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.shootingLeft, False), (self.rect.x, self.rect.y))
        pygame.draw.rect(screen, WHITE, self.rect, 2)

            
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image, hp):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
        self.image = pygame.transform.scale(image, character_size)
        self.width = character_width
        self.height = character_height
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        self.flip = False
        
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 6, self.rect.y + - 6))
        #pygame.draw.rect(screen, WHITE, self.rect, 2)

class Enemy(Character):
    #checkCollision with arrows
    def checkCollision(self):
        for arrow in arrow_group:
            if(arrow.rect.colliderect(self.rect)):
                self.hp -= 1
                arrow.kill()
        
        if self.hp <= 0:
            self.kill()

class Player(Character):
    def shoot(self):
        shotArrow = Arrow(self.rect.x, self.rect.y, self.flip, 1)
        return shotArrow

    def move(self):
        
        global hurtFlag
    #reset VARIABLES
        dx = 0
        dy = 0

    #process keypresses
        key = pygame.key.get_pressed()
        if(key[pygame.K_a]):
            dx -= character_movement_speed
            self.flip = True
        elif(key[pygame.K_d]):
            dx += character_movement_speed
            self.flip = False
        elif(key[pygame.K_s]):
            dy += character_movement_speed
        elif(key[pygame.K_w]):
            dy -= character_movement_speed
        
        if self.rect.x + dx > 0 and self.rect.right + dx < SCREEN_WIDTH:
           self.rect.x += dx
        
        if self.rect.y + dy > 0 and self.rect.bottom + dy < SCREEN_HEIGHT:
           self.rect.y += dy 

    #check collision with enemeis
        for enemy in enemy_group:
            if enemy.rect.colliderect(self.rect):
                if not hurtFlag:
                    self.hp -= 1
                    hurtFlag = True
                    self.image = pygame.transform.scale(player_hurt_image, character_size)
                    pygame.time.set_timer(hurtFlag_set, 500)
                    

character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, player_image, 3)

enemy_group = pygame.sprite.Group()

arrow_group = pygame.sprite.Group()

for e in range(10):
    enemy_x = random.randint(0, SCREEN_WIDTH - character_width)
    enemy_y = random.randint(0, SCREEN_HEIGHT - character_height)
    enemy = Enemy(enemy_x, enemy_y, enemy_image, 1)
    enemy_group.add(enemy)

run = True;
while run:
    
    clock.tick(FPS)

    screen.blit(bg_image, (0,0))

    for enemy in enemy_group:
        enemy.checkCollision()

    enemy_group.draw(screen)

    for arrow in arrow_group:
        arrow.move()
        arrow.killIfNoMoreBounces()

    arrow_group.draw(screen)

    character.move()
    character.draw()

    if character.hp <= 0:
        pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == hurtFlag_set:
            hurtFlag = False
            pygame.time.set_timer(hurtFlag_set, 0)
            character.image = pygame.transform.scale(player_image, character_size)
        if(event.type == pygame.KEYDOWN):
            if event.key == pygame.K_SPACE:
                arrow_group.add(character.shoot())

    pygame.display.flip()

pygame.quit()
