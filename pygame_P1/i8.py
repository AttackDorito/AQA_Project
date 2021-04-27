from pygame.constants import RESIZABLE, VIDEORESIZE
import pygame.display
from pygame.locals import *
from i8_classes import Body
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

config_file = open('config_file.txt', "r")
body_dict = {}
for x in config_file:
    line = (x.strip('\n').split(' = '))

    if line != ['']:
        body_dict[line[0]] = line[1]

    if len(body_dict) == 5:
        body_list.append(Body(
            float(body_dict['mass']),
            [float(body_dict['velocity'].split(',')[0]),float(body_dict['velocity'].split(',')[1])],
            [float(body_dict['position'].split(',')[0]),float(body_dict['position'].split(',')[1])],
            body_dict['image file'],name = body_dict['name'])
        )

        body_dict = {}






scale_factor = 1000
simulation_speed = 1

screen_offset = [0,0]
screen_size = [1080,720]


clock_counter = 0
phys_counter = 0

key_acceleration = 0

key_up = False
key_down = False
key_left = False
key_right = False
key_minus = False
key_plus = False
key_comma = False
key_period = False
key_[ = False   
key_]

while True:
    if clock_counter > 40:
        phys_framerate = phys_counter / clock_counter * 1000 * simulation_speed
        clock_counter = 0
        phys_counter = 0
        screen.blit(background,(0,0))
        for item in body_list:
           item.update_screen_pos(screen, screen_offset, scale_factor, screen_size)
        
        font.render_to(screen, (0,0), f"{round(phys_framerate,-3)},    {scale_factor}",(255,255,255))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            if event.type == KEYDOWN:
                if event.key ==K_LEFT:
                    key_left = True
                if event.key == K_RIGHT:
                    key_right = True
                if event.key == K_UP:
                    key_up = True
                if event.key == K_DOWN:
                    key_down = True
                if event.key == K_EQUALS:
                    key_plus = True
                if event.key == K_MINUS:
                    key_minus = True
                if event.key == K_COMMA:
                    key_comma = True
                if event.key == K_PERIOD:
                    key_period = True
                
            elif event.type == KEYUP:
                if event.key == K_LEFT:
                    key_left = False
                if event.key == K_RIGHT:
                    key_right = False
                if event.key == K_UP:
                    key_up = False
                if event.key == K_DOWN:
                    key_down = False
                if event.key == K_EQUALS:
                    key_plus = False
                if event.key == K_MINUS:
                    key_minus = False
                if event.key == K_COMMA:
                    simulation_speed -= 10
                    if simulation_speed < 1:
                        simulation_speed = 0.01
                    key_comma = False
                if event.key == K_PERIOD:
                    if simulation_speed <1:
                        simulation_speed = 1
                    else:
                        simulation_speed += 10
                    key_period = False

        if key_left:
            screen_offset[0] -= 4*scale_factor**2
        if key_right:
            screen_offset[0] += 4*scale_factor**2
        if key_up:
            screen_offset[1] -= 4*scale_factor**2
        if key_down:
            screen_offset[1] += 4*scale_factor**2

        if key_minus:      
            scale_factor += 1000 * key_acceleration
            key_acceleration += 0.1                          

        elif key_plus:
            scale_factor -= 1000 * key_acceleration
            key_acceleration += 0.1
            if scale_factor <1000:
                scale_factor = 1000

        else:
            key_acceleration = 0
        if event.type == VIDEORESIZE:
            screen_size = pygame.display.get_window_size()
            background = pygame.Surface(screen.get_size())
            background.fill((0,0,0))
    for index, item in enumerate(body_list):
            item.calculate_movement(body_list[index+1:], phys_step = simulation_speed)
    phys_counter += 1                
    clock_counter += clock.tick()