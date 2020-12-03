#Space Ware Pygame

# All constants/variables will be in ALL_CAPITAL_LETTERS


import pygame # documentation: https://www.pygame.org/docs/
import os
import time
import random


############################################################################################
# TASK 1: Setup Pygame window and its dimensions
############################################################################################
'''
Needed for Pygame window:
Width and height for screen
we set a name/title for the display
''' 
#Set dimension for gaming screen
WIDTH = 750
HEIGHT = 750 
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

# set title of gaming window
pygame.display.set_caption("Space Wars")

############################################################################################
# TASK 2: Load all images into the script
############################################################################################
'''
Pseudocode translate:

    from the pygame module, use the image.load method and, in there, we are going to
    load the image which is located at os.path.join(name of folder, name of img file)
    
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
BG = pygame.image.load(os.path.join("imgs", "bg_space.png"))