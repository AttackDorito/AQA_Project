from pygame.constants import RESIZABLE, VIDEORESIZE
import pygame.display
from pygame.locals import QUIT
from i5_classes import Body
from pygame import freetype

pygame.init()

clock = pygame.time.Clock()
clock.tick()
font = pygame.freetype.SysFont("Arial.ttf",24)
screen = pygame.display.set_mode((1080,720), RESIZABLE)        
pygame.display.set_caption('test window')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))



body_list = []

scale_factor = 10
screen_offset = [0,0]

screen_size = [1080,720]


planet_one = Body(10000e12, [0,0], [0,0],'planet.png')
body_list.append(planet_one)
planet_two = Body(10000e12, [0,1], [50000,0],'circle.png')
body_list.append(planet_two)
planet_three = Body(10000e12, [0,-1], [-50000,0], 'planet.png')
body_list.append(planet_three)

clock_counter = 0
phys_counter = 0

key_acceleration = 0

while True:
    if clock_counter > 40:
        phys_framerate = phys_counter / clock_counter * 1000
        clock_counter = 0
        phys_counter = 0
        screen.blit(background,(0,0))
        for item in body_list:
           item.update_screen_pos(screen, [0,0], scale_factor, screen_size)
           pygame.display.update(item.screen_pos)
           font.render_to(screen, (0,0), f"{round(phys_framerate,-3)}",(255,255,255))
    for index, item in enumerate(body_list):
        item.calculate_movement(body_list[index+1:])
    phys_counter += 1
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
            screen_offset[0] -= 2*scale_factor**2
        if keyRight:
            screen_offset[0] += 2*scale_factor**2
        if keyUp:
            screen_offset[1] += 2*scale_factor**2
        if keyDown:
            screen_offset[1] -= 2*scale_factor**2
        if keyMinus:                                
            if scale_factor <2:
                scale_factor = 2
            scale_factor += 10000 * key_acceleration
            key_acceleration += 0.1
        elif keyPlus:
            scale_factor -= 10000 * key_acceleration
            key_acceleration += 0.1
            if scale_factor <2:
                scale_factor = 2
        else:
            key_acceleration = 0
        if event.type == VIDEORESIZE:
            screen_size = pygame.display.get_window_size()
            background = pygame.Surface(screen.get_size())
            background.fill((0,0,0))
    clock_counter += clock.tick()