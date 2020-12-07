#Space Ware Pygame

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

    def draw(self): # method 



############################################################################################
# TASK 2: Setup Pygame Main Loop for future add-ins
############################################################################################

# drawing/ getting main loop setup to handle events
def main():
    run = True # dictates whether while loop below will run or not
    FPS = 60 #frames per second variable
    level = 1
    lives = 3
    main_font = pygame.font.SysFont("comicsans", 50) #pygame font type and size 


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

        #update window
        pygame.display.update() #refreshes the display 
 

    while run: 
        clock.tick(FPS) #'tick this clock based on the FPS rate given'
        #calling redraw_window
        redraw_window()

        #for loop to quit pygame window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False #when user quits the screen, then pygame stops running 

main()

