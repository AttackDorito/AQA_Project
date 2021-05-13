import pygame.display
from math import sqrt

class Body():
    def __init__(self,mass, vel, pos, image, name = 'default_object_name'):
        
        self.image = pygame.image.load("Assets/"+image)
        self._mass = mass
        self._pos = pos
        self._vel = vel
        self._force = [0,0]
        self.screen_pos = self.image.get_rect()
        self.name = name

    
    def _calculate_force(self, object_list, G = 6.67408e-11):
        for body in object_list:
            dist = sqrt((self._pos[0] - body._pos[0])**2 + (self._pos[1] - body._pos[1])**2)
            temp_force = [0,0]
            linear_force = G * (self._mass * body._mass) / (dist**2)
            temp_force[0] = (self._pos[0] - body._pos[0]) / dist * linear_force
            temp_force[1] = (self._pos[1] - body._pos[1]) / dist * linear_force
        
            if self._pos[0] > body._pos[0]:
                self._force[0] -= abs(temp_force[0])
                body._force[0] += abs(temp_force[0])
            else:
                self._force[0] += abs(temp_force[0])
                body._force[0] -= abs(temp_force[0])
            if self._pos[1] > body._pos[1]:
                self._force[1] -= abs(temp_force[1])
                body._force[1] += abs(temp_force[1])
            else:
                self._force[1] += abs(temp_force[1])
                body._force[1] -= abs(temp_force[1])

    def _apply_force(self,phys_step):
        accel = [(self._force[0]/self._mass),(self._force[1]/self._mass)]

        self._pos[0] += (self._vel[0] + (accel[0] /2)) * phys_step
        self._pos[1] += (self._vel[1] + (accel[1] /2)) * phys_step

        self._vel[0] += accel[0] * phys_step
        self._vel[1] += accel[1] * phys_step

        self._force = [0,0]
        
    def calculate_movement(self, object_list, phys_step = 1, G = 6.67408e-11):
        self._calculate_force(object_list)
        self._apply_force(phys_step)
        
    def update_screen_pos(self, screen, screen_offset, scale_factor, screen_size):
        self.screen_pos[0] = round(((self._pos[0] - screen_offset[0])/(scale_factor**2)) + screen_size[0]/2)
        self.screen_pos[1] = round(((self._pos[1] - screen_offset[1])/(scale_factor**2)) + screen_size[1]/2)
        screen.blit(self.image, self.screen_pos)
        
