import pygame.display


screen = pygame.display.set_mode((1080,720))        
pygame.display.set_caption('test window')

body_list = []

class Body():
    def __init__(self,pos=[0,0],image='star.png'):
        self.pos = pos
        self.image = pygame.image.load(image)
        body_list.append(self)
    

planet_one = Body(pos=[700,300], image='star.png')
planet_two = Body(pos=[100,100], image='circle.png')



while True:
    for item in body_list:
        screen.blit(item.image, item.pos)
    pygame.event.get()
    pygame.display.update()