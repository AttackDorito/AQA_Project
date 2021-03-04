import pygame.display


screen = pygame.display.set_mode((1080,720))        
pygame.display.set_caption('test window')

planet_img = pygame.image.load('planet.png')

while True:
    screen.blit(planet_img,(0,0))
    pygame.display.update()