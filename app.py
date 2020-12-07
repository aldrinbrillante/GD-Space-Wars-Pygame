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
    COOLDOWN = 1 #used for later 

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
        for laser in self.lasers: #method that will draw the lasers
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers: #for loop through all the lasers
            laser.move(vel) # move laser by the velocity
            if laser.off_screen(HEIGHT): #if laser off screen
                self.lasers.remove(laser) #delete laser
            elif laser.collision(obj): #if laser is colliding with obj
                obj.health -= 10 #health -10 
                self.lasers.remove(laser) #removes laser

    def cooldown(self): #handles counting the cooldown
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0 #not doing anything
        elif self.cool_down_counter > 0: #if it is greater than 0
            self.cool_down_counter += 1 #increment by 1

    def shoot(self):
        if self.cool_down_counter == 0: # we're not in the process of counting up to a specific cooldown
            laser = Laser(self.x-20, self.y, self.laser_img) #create a new laser...
            self.lasers.append(laser) #... and add it to the laser list
            self.cool_down_counter = 1 #then set the cooldown counter to start counting up 

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
    
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
     
    
    def draw(self, window):
        super().draw(window) #called parent draw method
        self.healthbar(window)
    
    def healthbar(self, window): # tc 14411
        #drew rectangles red and green based on health of hero
        pygame.draw.rect(window, (255,0,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width(), 10))
        pygame.draw.rect(window, (0,255,0), (self.x, self.y + self.ship_img.get_height() + 10, self.ship_img.get_width() * (self.health/self.max_health), 10))



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
    
def collide(obj1, obj2): #checks to see an overlap 
    offset_x = obj2.x - obj1.x #  this tells us the diff from object 1 and object 2
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

################################
# Laser Class
################################
class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    
    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0) #checks if laser is off

    def collision(self, obj):
        return collide(self, obj)


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
    lost_font = pygame.font.SysFont("comicsans", 200) #pygame font type and size for lost game

    enemies = [] #stores our enemies
    wave_length = 5

    hero_vel = 5 #velocity of hero --> to be called during 'if keys'
    enemy_vel = 3 #enemy velocity 1 pixel 
    laser_vel = 4

    #create hero variable with hero class and coordinates
    hero = Hero(300, 630)

    clock = pygame.time.Clock() # used to setup actual FPS

    lost = False #lost variable
    lost_count = 0

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

        if lost:
            lost_label = lost_font.render("GAME OVER!!", 1, (255,255,255))
            WINDOW.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350)) #centered in the screen

        #update window
        pygame.display.update() #refreshes the display 
 

    while run: 
        clock.tick(FPS) #'tick this clock based on the FPS rate given

        #calling redraw_window
        redraw_window()

        if lives <= 0 or hero.health <= 0:
            lost = True
            lost_count += 1 
        
        if lost:
            if lost_count > FPS * 5:
                run = False # if lost_count is greater than 5 secs, quits the game
            else:
                continue

        if len(enemies) == 0:
            level =+ 1 # as soon as no more enemies, level increases
            wave_length =+ 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-100), random.randrange(-1500, -100), random.choice(["red", "blue", "green"])) #spawns enemy at max left side of 50 and max right side of width-100
                enemies.append(enemy) #appends enemies


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
        if keys[pygame.K_s] and hero.y + hero_vel + hero.get_height() + 15 < HEIGHT: #down - if current y value + velocity is less thatn HEIGHT, then you can move
            hero.y += hero_vel
        #################################
        # hero's shoots with SPACE
        #################################
        if keys[pygame.K_SPACE]:
            hero.shoot()
        
        #########################################################
        # hero's movements with LEFT , RIGHT, UP, DOWN
        #########################################################
        if keys[pygame.K_LEFT] and hero.x - hero_vel > 0: #left
            hero.x -= hero_vel 
        if keys[pygame.K_RIGHT] and hero.x + hero_vel + hero.get_width() < WIDTH: #right
            hero.x += hero_vel
        if keys[pygame.K_UP] and hero.y - hero_vel > 0: #up 
            hero.y -= hero_vel 
        if keys[pygame.K_DOWN] and hero.y + hero_vel + hero.get_height() + 15 < HEIGHT: #down
            hero.y += hero_vel

        # move the enemies
        for enemy in enemies[:]:
            enemy.move(enemy_vel) #moving them down by their said velocity
            enemy.move_lasers(laser_vel, hero) #move it by velocity of laser and check if it hits hero

            #enemy shooting
            if random.randrange(0, 2*60) == 1: # 2*60 frames per second = 50% chance of shooting 
                enemy.shoot()
            
            # collision between player and ships
            if collide(enemy, hero):
                hero.health -= 10
                enemies.remove(enemy)
            elif enemy.y + enemy.get_height() > HEIGHT: #if enemy passes the bottom of screen
                lives -= 1 #subtract hero lives
                enemies.remove(enemy) #removes object from enemies list

        
        hero.move_lasers(-laser_vel, enemies) # this checks if laser has collided with any of the enemies...negative to make sure laser goes up

main()

