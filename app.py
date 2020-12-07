#Space Ware Pygame

# Resources:
# https://www.pygame.org/docs/ref/key.html

# All constants/variables will be in ALL_CAPITAL_LETTERS


import pygame # documentation: https://www.pygame.org/docs/
import os
import time
import random
pygame.font.init() #this tells pygame  to initialize font 

############################################################################################
# TASK 1: Setup Pygame window + Load all images into the script
############################################################################################
'''
Needed for Pygame window:
    Width and height for screen
    we set a name/title for the display
''' 
#Set dimension for gaming screen
WIDTH = 1200
HEIGHT = 750 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# set title of gaming WINDOW
pygame.display.set_caption("Space Wars")

'''
Pseudocode translate:

    Use pygame's image.load method and load the image,
    which is located at os.path.join(name of folder, name of img file)
'''
# RED_SHIP = pygame.image.load(imgs/enemy_red.png) is also another option 

#Enemies
RED_SHIP = pygame.image.load(os.path.join("imgs", "enemy_red.png"))
GREEN_SHIP = pygame.image.load(os.path.join("imgs", "enemy_green.png"))
BLUE_SHIP = pygame.image.load(os.path.join("imgs", "enemy_blue.png"))

#Hero
HERO = pygame.image.load(os.path.join("imgs", "hero.png"))

#Lasers
RED_LASER = pygame.image.load(os.path.join("imgs", "laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("imgs", "laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("imgs", "laser_blue.png"))
HERO_LASER = pygame.image.load(os.path.join("imgs", "laser_hero.png"))

#Background Image of Space
    # using pygame.transform.scale to scale x,y image for background 
BG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "space_bg.png")), (WIDTH, HEIGHT) )


############################################################################################
# TASK 3: Setup Ship Class
############################################################################################
class Ship: #abstract class. wont be used but only INHERITED
    def __init__(self, x, y, health=100):
        #attributes
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None #this will allow us to draw the img later
        self.laser_img = None #this will allow us to draw the img later
        self.lasers = []
        self.cool_down_counter = 0 #created so user can't spam lasers during game

    def draw(self, window): # method 
        window.blit(self.ship_img, (self.x, self.y))

    def get_width(self): #func to get width of hero
        return self.ship_img.get_width()

    def get_height(self): #func to get height of hero
        return self.ship_img.get_height()  

class Hero(Ship):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = HERO
        self.laser_img = HERO_LASER
        self.mask = pygame.mask.from_surface(self.ship_img) #mask allows for pixel perfect collision 
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = { #dictionary 
                "red": (RED_SHIP, RED_LASER),
                "green": (GREEN_SHIP, GREEN_LASER),
                "blue": (BLUE_SHIP, BLUE_LASER)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel): # if we pass the velocity to this method, we move the ship 
        self.y += vel
    





############################################################################################
# TASK 2: Setup Pygame Main Loop for future add-ins
############################################################################################

# drawing/ getting main loop setup to handle events
def main():
    run = True # dictates whether while loop below will run or not
    FPS = 60 #frames per second variable
    level = 0
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 50) #pygame font type and size 
    hero_vel = 5 #velocity of hero --> to be called during 'if keys'

    enemies = [] #stores our enemies
    wave_length = 5
    enemy_vel = 1 #enemy velocity 1 pixel 

    #create hero variable with hero class and coordinates
    hero = Hero(300, 650)

    clock = pygame.time.Clock() # used to setup actual FPS

    def redraw_window():
        WINDOW.blit(BG, (0, 0)) #blit allows make WINDOW surface to be placed/located at said coordinate: 0,0

        #draw text
        lives_display = main_font.render(f"Lives: {lives}", 1, (255,255,255)) #RGB-Red,Green,Blue  
        level_display = main_font.render(f"Level: {level}", 1, (255,255,255)) #RGB-Red,Green,Blue

        #display lives text
        WINDOW.blit(lives_display, (10,10))
        #display level text
        WINDOW.blit(level_display, (WIDTH - level_display.get_width() - 10,10))

        for enemy in enemies:
            enemy.draw(WINDOW)

        hero.draw(WINDOW)

        #update window
        pygame.display.update() #refreshes the display 
 

    while run: 
        clock.tick(FPS) #'tick this clock based on the FPS rate given'

        if len(enemies) == 0:
            level =+ 1 # as soon as no more enemies, level increases
            wave_length =+ 5
            for i in range(wave_length):


        #for loop to quit pygame window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #when user quits the screen, then pygame stops running 

        keys = pygame.key.get_pressed() #get the state of all keyboard buttons

        #################################
        # hero's movements with WASD
        #################################
        if keys[pygame.K_a] and hero.x - hero_vel > 0: #left
            #to move left i need to subtract from my x value of my player
            hero.x -= hero_vel # move {hero_vel} pixels to the left
        if keys[pygame.K_d] and hero.x + hero_vel + hero.get_width() < WIDTH: #right
            hero.x += hero_vel
        if keys[pygame.K_w] and hero.y - hero_vel > 0: #up - this makes sure we are not less than 0 when moving up
            hero.y -= hero_vel # subtracts the velocity bs starting position is 0,0 at top left
        if keys[pygame.K_s] and hero.y + hero_vel + hero.get_height() < HEIGHT: #down - if current y value + velocity is less thatn HEIGHT, then you can move
            hero.y += hero_vel
        
        #########################################################
        # hero's movements with LEFT , RIGHT, UP, DOWN
        #########################################################
        if keys[pygame.K_LEFT] and hero.x - hero_vel > 0: #left
            hero.x -= hero_vel 
        if keys[pygame.K_RIGHT] and hero.x + hero_vel + hero.get_width() < WIDTH: #right
            hero.x += hero_vel
        if keys[pygame.K_UP] and hero.y - hero_vel > 0: #up 
            hero.y -= hero_vel 
        if keys[pygame.K_DOWN] and hero.y + hero_vel + hero.get_height() < HEIGHT: #down
            hero.y += hero_vel

        #calling redraw_window
        redraw_window()

main()

