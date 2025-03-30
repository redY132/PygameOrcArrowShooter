import pygame
import array
import random
import math

pygame.init()

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

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
resolutionScale = int(math.ceil((SCREEN_WIDTH / 854) * 0.85))
character_size = (30 * resolutionScale, 40 * resolutionScale)
character_hitbox_error = -20 * resolutionScale
enemy_hitbox_error_x = 3* resolutionScale
enemy_hitbox_error_y = 0* resolutionScale
character_width = 30* resolutionScale 
character_height = 40* resolutionScale 
character_movement_speed = 4* resolutionScale
arrow_size_x = 22* resolutionScale
arrow_size_y = 12* resolutionScale
enemy_movement_speed = 3 * resolutionScale
MAX_ENEMIES = 10
hurtFlag = False
hurtFlag_set = pygame.USEREVENT
arrow_count = 5
arrow_bounce = 5
base_arrow_size = 2.5
arrow_size = base_arrow_size * resolutionScale * 0.25
arrow_speed = 5 * resolutionScale
arrow_cooldown = 100
arrow_off_cooldown = pygame.USEREVENT
arrow_can_shoot = True
sqrt_of_2 = 1.4142

bg_image = pygame.transform.scale_by(bg_image, int(math.ceil(SCREEN_WIDTH / 854)))

#COLORS
WHITE = (255,255,255)

class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y, shootingLeft, bounces, rotation):
        pygame.sprite.Sprite.__init__(self)

        #applying rotation and flip
        self.rotation = rotation

        scaledImage = pygame.transform.scale(
            arrow_image,
            (arrow_size_x * arrow_size, arrow_size_y * arrow_size))
        flippedImage = pygame.transform.flip(scaledImage, shootingLeft, not shootingLeft)
        self.image = pygame.transform.rotate(
            flippedImage,
            -self.rotation)

        self.rect = self.image.get_rect()
        self.dx = 0
        self.dy = 0
        
        self.rect.x = x
        self.rect.y = y
        self.shootingLeft = shootingLeft
        self.bounces = bounces

        direction = -arrow_speed if self.shootingLeft else arrow_speed

        self.dx = math.ceil(math.cos(math.radians(self.rotation)) * direction) 
        self.dy = math.ceil(math.sin(math.radians(self.rotation)) * direction)

    def move(self):
        # if(self.shootingLeft):
        #     curr_arrow_speed = -arrow_speed
        # else:
        #     curr_arrow_speed = arrow_speed
        #
        # self.dx = math.ceil(math.cos(math.radians(self.rotation)) * curr_arrow_speed) 
        # self.dy = math.ceil(math.sin(math.radians(self.rotation)) * curr_arrow_speed)

        #collision with enemy
        for enemy in enemy_group:

            withinXWhenShootingLeft = (enemy.rect.centerx > (self.rect.x + self.dx)) and (enemy.rect.centerx < (self.rect.x))        
            withinXWhenShootingRight = (enemy.rect.centerx < (self.rect.x + self.dx)) and (enemy.rect.centerx > (self.rect.x))
            withinY = ((self.rect.centery + self.dy) > enemy.rect.top) and ((self.rect.centery + self.dy) < enemy.rect.bottom)

            if ((withinXWhenShootingLeft if self.shootingLeft else withinXWhenShootingRight) and withinY) or enemy.rect.colliderect(self.rect):

                enemy.hp -= 1

                if(enemy.hp <= 0):
                    enemy.kill()

                self.kill()

                return

        def killIfNoMoreBounces():
            self.bounces -= 1
            if self.bounces < 0:
                self.kill()
                return True
            else:
                return False

        def flip():
            self.rotation = -self.rotation
            curr_direction = -arrow_speed if self.shootingLeft else arrow_speed
            self.dx = math.ceil(math.cos(math.radians(self.rotation)) * curr_direction) 
            self.dy = math.ceil(math.sin(math.radians(self.rotation)) * curr_direction)

        #bouncing
        if ((self.rect.x + self.dx <= 0) or (self.rect.x + self.dx >= SCREEN_WIDTH - 35 * resolutionScale)):
            if killIfNoMoreBounces():
                return
            self.shootingLeft = not self.shootingLeft
            flip()
            self.image = pygame.transform.flip(self.image, True, False)

        if ((self.rect.y + self.dy >= (SCREEN_HEIGHT - 25 * resolutionScale)) or (self.rect.y + self.dy <= 0)):
            if killIfNoMoreBounces():
                return
            flip()
            self.image = pygame.transform.flip(self.image, False, True)
            

        # elif :
        #     self.shootingLeft = not self.shootingLeft
        #     self.bounces -= 1

        #movement
        self.rect.x += self.dx
        self.rect.y += self.dy

        #correction
        if(self.rect.y >= SCREEN_HEIGHT - 25 * resolutionScale):
            self.rect.y = SCREEN_HEIGHT - 25 * resolutionScale;
        if(self.rect.y <= 0):
            self.rect.y = 0

        if(self.rect.x >= SCREEN_WIDTH - 35 * resolutionScale):
            self.rect.x = SCREEN_WIDTH - 35 * resolutionScale
        if(self.rect.x <= 0):
            self.rect.x = 0
    #
    # def draw(self):
    #     screen.blit(pygame.transform.flip(self.image, self.shootingLeft, False), (self.rect.x, self.rect.y))
    #     pygame.draw.rect(screen, WHITE, self.rect, 2)

            
class Character(pygame.sprite.Sprite):
    def __init__(self, x, y, image, hp, error_x, error_y):
        pygame.sprite.Sprite.__init__(self)
        self.hp = hp
        self.image = pygame.transform.scale(image, character_size)
        self.width = character_width + error_x
        self.height = character_height + error_y
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x,y)
        self.flip = False
    #     
    # def draw(self):
    #     screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x, self.rect.y + - 6))
    #    pygame.draw.rect(screen, WHITE, self.rect, 2)

class Enemy(Character):
    def move(self, character: Character):
        targetX = character.rect.centerx
        targetY = character.rect.centery
        distanceX = targetX - self.rect.centerx
        # distanceY = targetY - self.rect.centery
        # angle = math.atan(distanceY / (distanceX if (not (distanceX == 0)) else 1))
        # print(angle)
        # dx = 
        # dy

    #checkCollision with arrows
    # def checkCollision(self):
    #     for arrow in arrow_group:
    #         if(arrow.rect.colliderect(self.rect)):
    #             self.hp -= 1
    #             arrow.kill()
    #     
    #     if self.hp <= 0:
    #         self.kill()

class Player(Character):
    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 11, self.rect.y - 7))
        # pygame.draw.rect(screen, WHITE, self.rect, 2)
    #
    def shoot(self):
        global arrow_can_shoot

        if arrow_can_shoot:

            shotArrow_array = []

            if(self.flip):
                x = self.rect.x - 50
            else:
                x = self.rect.x 

            y = self.rect.y

            shotArrow_array.append(Arrow(x, y, self.flip, arrow_bounce, 0))

            for i in range(1, (arrow_count + 1) // 2):
                #add one arrow with positive rotation and one with negative
                angle = 90 / (arrow_count - 1)
                shotArrow1 = Arrow(x, y, self.flip, arrow_bounce, angle * i)
                shotArrow2 = Arrow(x, y, self.flip, arrow_bounce, -angle * i)

                shotArrow_array.append(shotArrow1)
                shotArrow_array.append(shotArrow2)

            arrow_can_shoot = False
            pygame.time.set_timer(arrow_off_cooldown, arrow_cooldown)
            return shotArrow_array
        else:
            return 0

    def takeInput(self):
        
        global hurtFlag
    #reset VARIABLES
        dx = 0
        dy = 0

    #process movement
        key = pygame.key.get_pressed()
        
    #multiply by sqrt if moving diagonally
        if key[pygame.K_a] and key[pygame.K_w]:
            self.flip = True
            dx -= character_movement_speed / sqrt_of_2
            dy -= character_movement_speed / sqrt_of_2
        elif key[pygame.K_a] and key[pygame.K_s]:
            self.flip = True
            dx -= character_movement_speed / sqrt_of_2
            dy += character_movement_speed / sqrt_of_2
        elif key[pygame.K_d] and key[pygame.K_w]:
            self.flip = False
            dx += character_movement_speed / sqrt_of_2 
            dy -= character_movement_speed / sqrt_of_2
        elif key[pygame.K_d] and key[pygame.K_s]:
            self.flip = False
            dx += character_movement_speed / sqrt_of_2
            dy += character_movement_speed / sqrt_of_2
        elif(key[pygame.K_a]):
            dx -= character_movement_speed
            self.flip = True
        elif(key[pygame.K_d]):
            dx += character_movement_speed
            self.flip = False
        elif(key[pygame.K_s]):
            dy += character_movement_speed
        elif(key[pygame.K_w]):
            dy -= character_movement_speed
        
    #boundaries
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

    #return arrows if space
        if key[pygame.K_SPACE]:
            return self.shoot()
        else:
            return 0

character = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, player_image, 3, character_hitbox_error, character_hitbox_error)

enemy_group = pygame.sprite.Group()

arrow_group = pygame.sprite.Group()

for e in range(MAX_ENEMIES):
    enemy_x = random.randint(0, SCREEN_WIDTH - character_width)
    enemy_y = random.randint(0, SCREEN_HEIGHT - character_height)
    enemy = Enemy(enemy_x, enemy_y, enemy_image, 1, enemy_hitbox_error_x, enemy_hitbox_error_y)
    enemy_group.add(enemy)

enemy1 = Enemy(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, enemy_image, 1, enemy_hitbox_error_x, enemy_hitbox_error_y)
enemy_group.add(enemy1)


run = True;
while run:

    clock.tick(FPS)

    # enemy1.move(character)   

    screen.blit(bg_image, (0,0))

    enemy_group.draw(screen)
 
    for arrow in arrow_group:
        arrow.move()

    arrow_group.draw(screen)

    returned_arrows = character.takeInput()
    if(returned_arrows != 0):
        for i in range(len(returned_arrows)):
            arrow_group.add(returned_arrows[i])

    character.draw()

    if character.hp <= 0:
        run = False
        #pygame.quit()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == hurtFlag_set:
            hurtFlag = False
            pygame.time.set_timer(hurtFlag_set, 0)
            character.image = pygame.transform.scale(player_image, character_size)
        if event.type == arrow_off_cooldown:
            arrow_can_shoot = True
            pygame.time.set_timer(arrow_off_cooldown, 0)

    pygame.display.flip()

pygame.quit()
