
import numpy as np
import pymunk
import pymunk.pyglet_util
import math

###########################################
# PhysicsObject
###########################################
class PhysicsObject:

    def __init__(self, object, width, height, mass=10, isRotatable=False, immovable=False, friction=1):
        
        self.o = object
        self.immovable = immovable
        self.width = width
        self.height = height

        self.mass = mass
        self.isRotatable = isRotatable

        if immovable:
            self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        else:
            self.body = pymunk.Body(self.mass)
        self.body.position = self.o.x + self.width/2, self.o.y + self.height/2

        self.poly = pymunk.Poly.create_box(self.body, (self.width, self.height))
        self.poly.mass = self.mass

        self.poly.friction = friction
        
    
    def addForce(self, x, y):
        self.body.apply_force_at_local_point((x,y))

    
    def update(self):
        if not self.isRotatable:
            self.body.angular_velocity = 0
            self.body.angle = 0

        self.o.x, self.o.y = self.body.position[0] - self.width/2, self.body.position[1] - self.height/2
