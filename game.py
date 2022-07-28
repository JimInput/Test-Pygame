import math
import random
import pygame

import pygame, sys
from pygame.locals import *

class Enemy:
    def __init__(self, x_position, y_position, y_velocity):
        self.x_position = x_position
        self.y_position = y_position
        self.y_velocity = y_velocity

class Pew:
    def __init__(self, x_position, y_position, x_velocity, isFlipped, isDisabled):
        self.x_position = x_position
        self.y_position = y_position
        self.x_velocity = x_velocity
        self.isFlipped = isFlipped
        self.isDisabled = isDisabled
        
class Refuel:
    def __init__(self, x_position, y_position, amount):
        self.x_position = x_position
        self.y_position = y_position
        self.amount = amount

def main():
    pygame.init()


    (width, height) = (640,480)

    clock = pygame.time.Clock()

    DISPLAY = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Game')

    characterTex = pygame.image.load('data/amongknife.png')

    enemyTex = pygame.image.load('data/rock.png')

    backgroundTex = pygame.image.load('data/background_2.png')

    pewTex = pygame.image.load('data/pew.png')

    frameTex = pygame.image.load('data/emptygauge.png')

    halfFuelTex = pygame.image.load('data/fuelup50.png')

    winTex = pygame.image.load('data/win_screen.png')

    font = pygame.font.Font('data/da.ttf', 40)

    WHITE = (255,255,255)
    BLUE = (0,0,255)

    x_position = 640 / 2 - 32 / 2
    y_position = 480 / 2 - 32 /2
    x_velocity = 0
    y_velocity = 0

    boost = 1
    fuel = 1

    score = 0

    is_fuel_on_field = False

    change_in_time = 0

    wave_one = False
    wave_two = False
    
    field_fuel = Refuel(0,0,0)

    enemies = []
    pewers = []
    for i in range (8):
        enemies.append(Enemy(random.randint(0, 640 - 32), -random.randint(32, 256), random.randint(1,10)/2))



    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            x_velocity = 2 * boost
        if keys[pygame.K_LEFT]:
            x_velocity = -2 * boost
        if keys[pygame.K_UP]:
            y_velocity = -2 * boost
        if keys[pygame.K_DOWN]:
            y_velocity = 2 * boost
        if (keys[pygame.K_LCTRL] and fuel > 0):
            boost = 2
            fuel = fuel - 0.005
        elif (fuel <= 0):
            boost = 1
            fuel = 0
        if (keys[pygame.K_LCTRL] == False or fuel <= 0):
            boost = 1

        if keys[pygame.K_x]:
            backgroundTex = pygame.image.load('data/background_2.png')
        if keys[pygame.K_c]:
            backgroundTex = pygame.image.load('data/background.png')


        x_position = x_position + x_velocity
        y_position = y_position + y_velocity

        x_velocity = 0
        y_velocity = 0

        total_time = pygame.time.get_ticks()

        game_time = total_time - change_in_time
        


        for enemy in enemies:
            enemy.y_position = enemy.y_position + enemy.y_velocity

            if enemy.y_position > 480:
                enemy.x_position = random.randint(0, 640 - 32)
                enemy.y_position = -32
                enemy.y_velocity = random.randint(10,50)/10
                score = score + 1

            if (boost != 2 and x_position + 32 > enemy.x_position and x_position < enemy.x_position + 32 and y_position + 32 > enemy.y_position and y_position < enemy.y_position + 32):
                change_in_time = total_time
                wave_one = False
                wave_two = False
                x_position, y_position, fuel, score, enemies, pewers, is_fuel_on_field, wave_one, wave_two= reset()

        
        if (game_time > 10000 and wave_one == False):
            gen_pewers(pewers)
            wave_one = True

        
        if (game_time > 25000 and wave_two == False):
            gen_pewers(pewers)
            wave_two = True

        for pew in pewers:
            pew.x_position = pew.x_position + pew.x_velocity
            if (pew.isFlipped == False and pew.isDisabled == False):
                if (pew.x_position > 640 and pew.isDisabled != True):
                    score = score + 1
                    pew.x_position = -32
                    pew.y_position = random.randint(32,450)
                    pew.y_velocity = random.randint(3,5)
                    # pew.isDisabled = True
                    
            elif (pew.isFlipped == True and pew.isDisabled == False):
                if (pew.x_position + 40 < 0 and pew.isDisabled != True):
                    score = score + 1
                    pew.x_position = 640 + 32
                    pew.y_position = random.randint(32,450)
                    pew.y_velocity = -random.randint(3,5)
                    # pew.isDisabled = True
            
            if (boost != 2 and pew.isDisabled == False and x_position + 32 > pew.x_position and x_position < pew.x_position + 40 and y_position + 32 > pew.y_position and y_position < pew.y_position + 20):
                change_in_time = total_time
                x_position, y_position, fuel, score, enemies, pewers, is_fuel_on_field, wave_one, wave_two= reset()

        if (fuel <= .45 and is_fuel_on_field == False):
            field_fuel.x_position = random.randint(0, 640 - 20)
            field_fuel.y_position = random.randint(240, 480 - 20)
            field_fuel.amount = 50
            is_fuel_on_field = True

        if (is_fuel_on_field and x_position + 32 > field_fuel.x_position and x_position < field_fuel.x_position + 20 and y_position + 32 > field_fuel.y_position and y_position < field_fuel.y_position + 20):
            fuel = fuel + 0.5
            is_fuel_on_field = False

        #
        DISPLAY.blit(backgroundTex, (0,0))
        DISPLAY.blit(characterTex, (x_position,y_position))

        if (is_fuel_on_field and field_fuel.amount == 50):
            DISPLAY.blit(halfFuelTex, (field_fuel.x_position, field_fuel.y_position))

        for enemy in enemies:
            DISPLAY.blit(enemyTex, (enemy.x_position, enemy.y_position))

        for pew in pewers:
            if (pew.isFlipped == False and pew.isDisabled == False):
                DISPLAY.blit(pewTex, (pew.x_position, pew.y_position))
            elif (pew.isFlipped == True and pew.isDisabled == False):
                DISPLAY.blit(pygame.transform.flip(pewTex, True, False), (pew.x_position, pew.y_position))

        

        # if (fuel <= 1 and fuel > 0.75):
        #     DISPLAY.blit(fullTex, (640 - fullTex.get_width(), 0))
        # elif (fuel <= 0.75 and fuel > 0.50):
        #     DISPLAY.blit(qETex, (640 - fullTex.get_width(), 0))
        # elif (fuel <= 0.50 and fuel > 0.25):
        #     DISPLAY.blit(halfTex, (640 - fullTex.get_width(), 0))
        # elif (fuel <= 0.25 and fuel > 0):
        #     DISPLAY.blit(qFTex, (640 - fullTex.get_width(), 0))
        # elif (fuel == 0):
        #     DISPLAY.blit(emptyTex, (640 - fullTex.get_width(), 0))  

        # if (fuel < 0):
        #     fuel = 0

        DISPLAY.blit(frameTex, (640 - 20, 0))
        pygame.draw.rect(DISPLAY, (0,255,0), pygame.Rect(622, 102 - fuel * 100, 16, fuel * 100))
        
        
        fuel_text = font.render(str((fuel * 100).__round__()) + '%', True, (0,0,0))
        DISPLAY.blit(fuel_text, (640 - frameTex.get_width() - fuel_text.get_width(), 0))
        
        score_text = font.render(str(score), True, (0,0,0))
        DISPLAY.blit(score_text, (640/2 - score_text.get_width() / 2,0))

        fps_text = font.render('FPS: ' + str(clock.get_fps().__round__()), True, (0,0,0))
        DISPLAY.blit(fps_text, (5, 480 - fps_text.get_height()))

        timer_text = font.render((timeConfig(game_time)), True, (0,0,0))
        DISPLAY.blit(timer_text, (640/2 - timer_text.get_width() / 2,480 - timer_text.get_height() ))

        # print(fuel)
        # print(total_time)
        # print(change_in_time)
        # print(game_time)
        # print(wave_one)

        if (game_time >= 60000):
            pewers = []
            enemies = []
            DISPLAY.blit(winTex, (0,0))
        
        if keys[pygame.K_w]:
            change_in_time = total_time
            x_position, y_position, fuel, score, enemies, pewers, is_fuel_on_field, wave_one, wave_two= reset()

        pygame.display.update()

def gen_pewers(pewers):
    print("genning pewers")
    for i in range(3):
        side = random.randint(1,2)
        if (side == 1):
            pewers.append(Pew(-random.randint(32, 256), random.randint(32,450),random.randint(3,5), False, False))
        elif (side == 2):
            pewers.append(Pew(640 + random.randint(32, 256), random.randint(32,450),-random.randint(3,5), True, False))

def reset():
    x_position = 640/2 - 32/2
    y_position = 480/2 - 32/2
    score = 0
    enemies = []
    pewers = []
    wave_one = False
    wave_two = False
    
    for i in range (8):
        enemies.append(Enemy(random.randint(0, 640 - 32), -32, random.randint(10,50)/10))
    fuel = 1
    fieldFuel = False
    
    
    return x_position,y_position,fuel,score,enemies,pewers, fieldFuel, wave_one, wave_two

def timeConfig(miliseconds):
    milis = miliseconds
    seconds = milis / 1000
    minutes = math.floor((seconds / 60))
    if (math.floor(seconds) - 60 * minutes < 10): return str(minutes) + ':0' + str(math.floor(seconds) - 60 * minutes)
    return str(minutes) + ':' + str(math.floor(seconds) - 60 * minutes)

main()