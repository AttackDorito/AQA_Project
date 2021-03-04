import pygame.display
from math import sqrt

class Body():
    def __init__(self,mass = 1000, vel = [0,0], pos=[0,0], image='star.png', list_index=0):
        self.screen_pos = pos
        self.image = pygame.image.load(image)
        self._list_index = list_index
        self._mass = mass
        self._pos = pos
        self._vel = vel
        self._force = [0,0]

    
    def calculate_movement(self, object_list, phys_step = 1, G = 6.67408e-11):
        for body in object_list[self._list_index+1:]:
            dist = sqrt((self._pos[0] - body.pos[0])**2 + (self._pos[1] - body.pos[1])**2)
            temp_force = [0,0]
            linear_force = G * (self._mass + body._mass) / (dist**2)
            temp_force[0] = (self._pos[0] - body.pos[0]) / dist * linear_force
            temp_force[1] = (self._pos[1] - body.pos[1]) / dist * linear_force
        
            if self._pos[0] > body.pos[0]:
                self._force[0] -= abs(temp_force[0])
                body._force[0] += abs(temp_force[0])
            else:
                self._force[0] += abs(temp_force[0])
                body._force[0] -= abs(temp_force[0])
            if self._pos[1] < body.pos[1]:
                self._force[1] -= abs(temp_force[1])
                body._force[1] += abs(temp_force[1])
            else:
                self._force[1] += abs(temp_force[1])
                body._force[1] -= abs(temp_force[1])
        
        accel = [(self._force[0]/self._mass),(self._force[0]/self._mass)]

        self._pos[0] += self._vel[0] + (accel[0] * phys_step/2)
        self._pos[1] += self._vel[1] + (accel[1] * phys_step/2)

        self._vel[0] += accel[0] * phys_step
        self._vel[1] += accel[1] * phys_step

        self._force = [0,0]

