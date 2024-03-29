from pygame.constants import RESIZABLE, VIDEORESIZE
import pygame.display
from pygame.locals import QUIT
from i4_classes import Body


screen = pygame.display.set_mode((1080,720), RESIZABLE)        
pygame.display.set_caption('test window')
background = pygame.Surface(screen.get_size())
background = background.convert()
background.fill((0,0,0))



body_list = []
scale_factor = 1000

screen_size = [1080,720]

planet_one = Body(6e24, [0,0], [0,0],'circle.png')
body_list.append(planet_one)
planet_two = Body(7e22, [0,1000], [384402000,0],'star.png')
body_list.append(planet_two)

i =1
while True:
    if i == 1000:
        i = 0
        #screen.blit(background,(0,0))
        for item in body_list:
           item.update_screen_pos(screen, [0,0], scale_factor, screen_size)
           pygame.display.update(item.screen_pos)
    for index, item in enumerate(body_list):
        item.calculate_movement(body_list[index+1:])
    for event in pygame.event.get():    # fetches event queue
        if event.type == QUIT:          # checks if the window has been closed    
            quit()                      # exits the program.
        if event.type == VIDEORESIZE:
            screen_size = pygame.display.get_window_size()
            background = pygame.Surface(screen.get_size())
            background.fill((0,0,0))
            
    i += 1