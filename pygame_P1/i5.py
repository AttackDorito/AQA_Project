from pygame.constants import RESIZABLE, VIDEORESIZE
import pygame.display
from pygame.locals import QUIT
from i5_classes import Body
from pygame import freetype

pygame.init()

clock = pygame.time.Clock()
clock.tick()
phys_clock = pygame.time.Clock()
phys_clock.tick()
font = pygame.freetype.SysFont("Arial.ttf",24)
screen = pygame.display.set_mode((1080,720), RESIZABLE)        
pygame.display.set_caption('test window')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))



body_list = []
scale_factor = 5
simspeed = 100000

screen_size = [1080,720]

planet_one = Body(10000e12, [0,0], [0,0],'planet.png')
body_list.append(planet_one)
planet_two = Body(10000, [0,0.1], [5000,0],'circle.png')
body_list.append(planet_two)

clock_counter = 0
phys_counter = 0

while True:
    if clock_counter > 200:
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
    for event in pygame.event.get():    # fetches event queue
        if event.type == QUIT:          # checks if the window has been closed    
            quit()                      # exits the program.
        if event.type == VIDEORESIZE:
            screen_size = pygame.display.get_window_size()
            background = pygame.Surface(screen.get_size())
            background.fill((0,0,0))
    clock_counter += clock.tick()