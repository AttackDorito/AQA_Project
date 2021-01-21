from math import sqrt
import queue
import pygame
import sys
from pygame.locals import *
import time
from pygame import freetype
pygame.init()
screen = pygame.display.set_mode((1080,720))
pygame.display.set_caption('physics thing')

background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))

screen.blit(background,(0,0))
pygame.display.flip()

circle = pygame.image.load('circle.png')
planetimg = pygame.image.load('planet.png')

clock = pygame.time.Clock()
clock.tick()

G = 6.6743 * (10**-11) #gravitational constant
objectList = [] #list of all objects

xMove = 0
yMove = 0
scaleFactor = 10000 #number of metres per pixel
phystime = 10 #physics frame time in seconds

keyPlus = False
keyMinus = False
keyUp = False
keyDown = False
keyLeft = False
keyRight = False
class Body():       #A body affected by gravitational forces
    def __init__(self,mass,velxy,posxy,image):            #mass in kg , velocity in vertical and horizontal components (m/s) , position, image path
        self.mass = mass
        self.velxy = velxy
        self.posxy = posxy
        self.index = len(objectList)
        objectList.append(self)
        self.force = [0,0]
        self.accel = [0,0]
        self.pos = image.get_rect()
        self.image = image
        
    def calculate(self):        #calculates where the body will be next frame (does not move)
        self.force = [0,0]
        for body in objectList:
            if body.index == self.index:
                continue
            tempForce = [0,0]

            rad = sqrt((self.posxy[0] - body.posxy[0])**2 + (self.posxy[1] - body.posxy[1])**2)

            Force = (G*self.mass*body.mass)/(rad**2)
            tempForce[0] = Force * ((self.posxy[0] - body.posxy[0])/rad)
            tempForce[1] = Force * ((self.posxy[1] - body.posxy[1])/rad)

            
            if self.posxy[0] > body.posxy[0]:
                self.force[0] -= abs(tempForce[0])
            else:
                self.force[0] += abs(tempForce[0])
                
                
            if self.posxy[1] > body.posxy[1]:
                self.force[1] -= abs(tempForce[1])
            else:
                self.force[1] += abs(tempForce[1])

        self.accel[0] = self.force[0] / self.mass
        self.accel[1] = self.force[1] / self.mass

    def frame(self):        #moves the body to the new position
        self.posxy[0] += ((self.velxy[0]*phystime) + (0.5*self.accel[0])*phystime)
        self.posxy[1] += (-(self.velxy[1]*phystime) + (0.5*self.accel[1])*phystime)
        self.velxy[0] += (self.accel[0]*phystime)
        self.velxy[1] += (self.accel[1]*phystime)
    def drawFrame(self):
        self.frame()
        self.pos.centerx = round((self.posxy[0] - xMove)/scaleFactor**2) + 540
        self.pos.centery = -round((self.posxy[1] - yMove)/scaleFactor**2) + 360



def scaleFormat(scale):
    return f"{scale/1000000} Mm"

font = pygame.freetype.SysFont("Arial.ttf",24)

#sun = Body((1.989*10**30),[0,0],[-(148*10**6),0],circle)
earth = Body((5.972*10**24),[0,0],[0,0],planetimg)
moon = Body((7.348*10**22),[0,1022],[384402000,0],circle)

def nextFrame():
    for item in objectList:
        item.calculate()
    for item in objectList:
        item.frame()
        
for item in objectList:
    pass
    #item.pos = item.pos.move(540,360)
secondCount = 0
yearCount = 0
clockCounter = 0

while True:
    secondCount += phystime
    if secondCount == 31557600:
            secondCount = 0
            yearCount += 1
    clockCounter += clock.tick()
    if clockCounter > 14:
        clockCounter = 0
        clock.tick()
        screen.blit(background,(0,0,400,50))
        font.render_to(screen,(0,0),f"{round(secondCount/86400,1)}d, {yearCount} y {scaleFormat(1080*scaleFactor)} Metres across \n earth {list(map(round,earth.posxy))} \n moon {list(map(round,moon.posxy))}",(255,255,255))
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
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

        if keyLeft:
            xMove -= 2*scaleFactor**2
        if keyRight:
            xMove += 2*scaleFactor**2
        if keyUp:
            yMove += 2*scaleFactor**2
        if keyDown:
            yMove -= 2*scaleFactor**2
        if keyMinus:
            scaleFactor += 1000
        if keyPlus:
            scaleFactor -= 1000
            if scaleFactor < 1:
                scaleFactor = 1
        
        for item in objectList:
            pass
            #screen.blit(background, item.pos, item.pos)
        for item in objectList:
            item.calculate()
        for item in objectList:
            item.drawFrame()
            screen.blit(item.image, item.pos)
        pygame.display.update()
    else:
        nextFrame()
