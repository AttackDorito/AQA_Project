from math import sqrt         # imports square root function from the math module
import pygame                 # imports pygame library
from pygame.locals import *   # imports the pygame locals library
from pygame import freetype   # imports pygame freetype font handling module
pygame.init()                 # initialises pygame
screen = pygame.display.set_mode((1920,1080))        # creates the display window with a resolution of 1920 x 1080
pygame.display.set_caption('gravity simulation')     # sets the title of the window to 'gravity simulation'

background = pygame.Surface(screen.get_size())       # creates the background object
background = background.convert()                     
background.fill((0,0,0))                             # fills the background with black

screen.blit(background,(0,0))                        # updates the screen surface with the background
pygame.display.flip()                                # updates the window to display the changes to the user

moon_img = pygame.image.load('circle.png')             # loads icons to represent the objects
planet_img = pygame.image.load('planet.png')          # "
star_img = pygame.image.load('star.png')

clock = pygame.time.Clock()                          # creates a clock object which keeps track of the time since the last tick
clock.tick()                                         # staarts the clock

G = 6.6743 * (10**-11)      # gravitational constant
objectList = []             # list of all objects

xMove = 0
yMove = 0
scaleFactor = 1000          # number of metres per pixel
phystime = 10             # physics frame time in seconds

keyPlus = False
keyMinus = False
keyUp = False
keyDown = False
keyLeft = False
keyRight = False

class Body():                                         # A body affected by gravitational forces
    def __init__(self,mass,velxy,posxy,image):        # mass in kg , velocity in vertical and horizontal components (m/s) , position, image path
        self.mass = mass
        self.velxy = velxy
        self.posxy = posxy
        self.index = len(objectList)
        objectList.append(self)                      # adds itself to the list of objects
        self.force = [0,0]
        self.accel = [0,0]
        self.pos = image.get_rect()
        self.image = image
        
    def calculate(self):                             # calculates the net acceleration of the body                           # resets force to 0
        for body in objectList[self.index:]:                      # iterates through all simulated bodies 
            if body.index == self.index:             # skips calculating force for itself
                continue                
            tempForce = [0,0]                   

            rad = sqrt((self.posxy[0] - body.posxy[0])**2 + (self.posxy[1] - body.posxy[1])**2) # calculates distance between the objects

            Force = (G*self.mass*body.mass)/(rad**2)                                            # calculates the force the objects exert on each other
            tempForce[0] = Force * ((self.posxy[0] - body.posxy[0])/rad)                        #\
            tempForce[1] = Force * ((self.posxy[1] - body.posxy[1])/rad)                        #/ calculates the force as a 2d vector

            
            if self.posxy[0] > body.posxy[0]:                                                   # adds the force  on the x axis to the total    
                self.force[0] -= abs(tempForce[0])
                body.force[0] += abs(tempForce[0])                                              
            else:
                self.force[0] += abs(tempForce[0])
                body.force[0] -= abs(tempForce[0])
                

            if self.posxy[1] < body.posxy[1]:                                                   # adds the force on the y axis to the total
                self.force[1] -= abs(tempForce[1])
                body.force[1] += abs(tempForce[1])
            else:
                self.force[1] += abs(tempForce[1])
                body.force[1] -= abs(tempForce[1])

        self.accel[0] = self.force[0] / self.mass                                               # finds the x,y components of the acceleration of the body
        self.accel[1] = self.force[1] / self.mass
        print(f"calculated {self.mass}")                                             #

    def frame(self):                                                                            # applies the acceleration calculated in the calculate function
        self.posxy[0] += ((self.velxy[0]*phystime) + (0.5*self.accel[0])*phystime)              # and updates the position of the object
        self.posxy[1] += (-(self.velxy[1]*phystime) + (0.5*self.accel[1])*phystime)
        self.velxy[0] += (self.accel[0]*phystime)
        self.velxy[1] += (self.accel[1]*phystime)
        self.force = [0,0]
    def drawFrame(self):
        self.frame()
        try:                                                                                    # prevents crash due to zooming in too fast
            self.pos.centerx = round((self.posxy[0] - xMove)/scaleFactor**2) + 960              # assigns the object an on-screen position relative to it's actual postition
            self.pos.centery = -round((self.posxy[1] - yMove)/scaleFactor**2) + 540             # and the position of the viewport
        except:
            pass


def scaleFormat(scale):                                                                         
    return f"{scale/1000000} Mm"                                                                # formats the scale in a more readable way

font = pygame.freetype.SysFont("Arial.ttf",24)                                                  # sets up the font for drawing onscreen

sun = Body((1.989e+30),[0,0],[0,0],star_img)                                        # 
earth = Body((5.972*10**24),[0,-29780],[149600000000,0],planet_img)                                              # defining bodies to be simulated
moon = Body((7.348*10**22),[0,-1022-29780],[384402000+149600000000,0],moon_img)                                       # 

objectList.reverse()

def nextFrame():                                                                                # calculates for every object and then updates their positions
    for item in objectList:
        item.calculate()
    for item in objectList:
        item.frame()

secondCount = 0
yearCount = 0
clockCounter = 0
keyAcceleration = 0

while True:                                                                                     # main loop
    secondCount += phystime
    if secondCount == 31557600:                                                                 # increments year counter and resets second counter
            secondCount = 0
            yearCount += 1
    clockCounter += clock.tick()
    if clockCounter > 16:                                                                       # limits program to only drawing at 60fps
        clockCounter = 0
        clock.tick()                                                                            # starts the clock again
        screen.blit(background,(0,0))                                                    # blacks out the text
        font.render_to(screen,(0,0),f"{round(secondCount/86400,1)}d, {yearCount} y {scaleFormat(1920*scaleFactor)} across",(255,255,255)) # shows the time elapsed and the scale of the screen
        for event in pygame.event.get():                   # gets keyboard and mouse inputs
            if event.type == QUIT:                         # ends program if the window is closed
                exit()
            if event.type == KEYDOWN:                      # toggles key state if key is pressed or released
                if event.key ==K_LEFT:
                    keyLeft = True
                if event.key == K_RIGHT:
                    keyRight = True
                if event.key == K_UP:
                    keyUp = True
                if event.key == K_DOWN:
                    keyDown = True
                if event.key == K_EQUALS:
                    keyPlus = True
                if event.key == K_MINUS:
                    keyMinus = True
                    
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    keyLeft = False
                if event.key == K_RIGHT:
                    keyRight = False
                if event.key == K_UP:
                    keyUp = False
                if event.key == K_DOWN:
                    keyDown = False
                if event.key == K_EQUALS:
                    keyPlus = False
                if event.key == K_MINUS:
                    keyMinus = False

        if keyLeft:                                 # moves the viewpoint proportional to the zoom factor
            xMove -= 2*scaleFactor**2
        if keyRight:
            xMove += 2*scaleFactor**2
        if keyUp:
            yMove += 2*scaleFactor**2
        if keyDown:
            yMove -= 2*scaleFactor**2
        if keyMinus:                                
            if scaleFactor <2:
                scaleFactor = 2
            scaleFactor += 10000 * keyAcceleration       #increasees zoom speed the longer the key is held
            keyAcceleration += 0.1
        elif keyPlus:
            scaleFactor -= 10000 * keyAcceleration
            keyAcceleration += 0.1
            if scaleFactor <2:
                scaleFactor = 2
        else:
            keyAcceleration = 0
        for item in objectList:
            item.calculate()
        for item in objectList:
            item.drawFrame()
            screen.blit(item.image, item.pos)           # draws the objects to the screen
        pygame.display.update()
    else:
        nextFrame()
