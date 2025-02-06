
from .engine import Engine
from .collider import Collider
from .physics import PhysicsObject
from pyglet.shapes import Rectangle

class ControllablePlayer:

    def __init__(self, engine:Engine, x=300, y=300, w=50, h=50, mass=60):
        self.x = y
        self.y = x
        self.w = w
        self.h = h

        self.rect = Rectangle(x, y, w, h, color=(198, 39, 114))
        self.collider = Collider(x, y, w, h, self)
        self.physics = PhysicsObject(self, self.collider, mass)

        # reference
        self.engine = engine


    def __update__(self):
        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self):
        self.rect.draw()


    def update(self):
        
        force = 100

        # bevæg den
        if self.engine.isKeyPressed('w'):
            self.physics.addForce(0, force)

        if self.engine.isKeyPressed('s'):
            self.physics.addForce(0, -force)
        
        if self.engine.isKeyPressed('a'):
            self.physics.addForce(-force, 0)
        
        if self.engine.isKeyPressed('d'):
            self.physics.addForce(force, 0)

        self.__update__()

