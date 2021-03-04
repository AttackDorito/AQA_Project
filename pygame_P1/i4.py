import pygame.display
from pygame.locals import QUIT
from i4_classes import Body


screen = pygame.display.set_mode((1080,720))        
pygame.display.set_caption('test window')

body_list = []

planet_one = Body(pos=[700,300], image='star.png')
body_list.append(planet_one)
planet_two = Body(pos=[100,100], image='circle.png')
body_list.append(planet_two)


while True:
    for item in body_list:
        screen.blit(item.image, item.screen_pos)
    for event in pygame.event.get():    # fetches event queue
        if event.type == QUIT:          # checks if the window has been closed    
            quit()                      # exits the program.
    pygame.display.update()