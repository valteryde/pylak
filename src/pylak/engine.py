
# Den her kode base er en simpel version af en game engine.
# Den er skrevet i Python og bruger Pyglet til at håndtere vinduer og grafik.

import pyglet as pgl
from pyglet.shapes import Rectangle, Circle, Line, Arc, Ellipse, Triangle, Polygon, BezierCurve
from typing import DefaultDict
import numpy as np
import math

###########################################
# Engine
# TODO:
# - Smooth scene transitions
###########################################
class Engine:
    def __init__(self):
        self._width = 600
        self._height = 600
        
        self.window = pgl.window.Window(self._width, self._height)
        self._currentScene = None
        self._keyboard = pgl.window.key.KeyStateHandler()
        self.__keyNames = {v: k for k, v in pgl.window.key._key_names.items()}

        self._colliders = []
        self._physicsObjects = []


    # event handling
    def isKeyPressed(self, key:str) -> bool:

        keyval = self.__keyNames.get(key.upper())

        if keyval is None:
            return False

        return self._keyboard[keyval]
        
    
    # collider handling
    def addCollider(self, collider):
        self._colliders.append(collider)
    
    # add physics object
    def addPhysicsObject(self, physicsObject):
        self._physicsObjects.append(physicsObject)

    
    def isColliding(self, collider1, collider2) -> bool:
        return self.collisions[collider1].__contains__(collider2)

    
    # scene handling
    def setCurrentScene(self, scene):
        self._currentScene = scene
        self._colliders = []
        self._physicsObjects = []
        scene.setup()


    def __calculateCollisions__(self):
        
        self.collisions = DefaultDict(set)

        rows = 10
        cols = 10

        w, h = self._width/rows, self._height/cols

        matrix = [[[] for _ in range(cols)] for _ in range(rows)]

        # divide
        for collider in self._colliders:
            
            x0 = int(collider.x / w)
            y0 = int(collider.y / h)

            x1 = int((collider.x + collider.width) / w) + 1
            y1 = int((collider.y + collider.height) / h) + 1

            for x in range(x0, x1):
                for y in range(y0, y1):
                    
                    if x < 0 or x >= cols or y < 0 or y >= rows:
                        continue

                    matrix[x][y].append(collider)

        # check collision
        for x in range(cols):
            
            for y in range(rows):

                colliders = matrix[x][y]

                for i in range(len(colliders)):
                    for j in range(i+1, len(colliders)):
                        if colliders[i].isColliding(colliders[j]):
                            self.collisions[colliders[i]].add(colliders[j])
                            self.collisions[colliders[j]].add(colliders[i])

    # loop
    def __update__(self, dt):
        
        self.__calculateCollisions__()

        for physicsObject in self._physicsObjects:
            physicsObject.update(self, dt)

        self._currentScene.update()

    
    def __draw__(self):
        self.window.clear()
        self._currentScene.draw()


    def start(self):
        
        self.window.on_draw = self.__draw__

        self.window.push_handlers(self._keyboard)
        pgl.clock.schedule_interval(self.__update__, 1/60)
        pgl.app.run()




###########################################
# Collider 
###########################################
class Collider:
    
    def __init__(self, x, y, width, height, referenceObject):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pgl.shapes.Rectangle(x, y, width, height, color=(255, 0, 0))

        self.referenceObject = referenceObject


    def draw(self):
        self.rect.x = self.x
        self.rect.y = self.y

        self.rect.draw()


    def isColliding(self, other):
        return not (self.x + self.width < other.x or
                self.x > other.x + other.width or
                self.y + self.height < other.y or
                self.y > other.y + other.height)


###########################################
# PhysicsObject
###########################################
class PhysicsObject:

    def __init__(self, object, collider, mass=100, immovable=False, drag=0.5):
        self.collider = collider # use objects collider
        self.collider._physicsObject = self # add reference to physics object in collider
        self.object = object
        self.immovable = immovable

        # add x and y to objects
        object.x = collider.x
        object.y = collider.y

        self.collider._lastpos = [collider.x, collider.y]

        self.mass = mass

        self.velocity = np.array([0.0,0.0])
        self.forces = np.array([0.0,0.0])

        self.drag = drag * mass
        

    def addForce(self, x, y):
        self.forces += np.array([x, y])
    

    def update(self, engine:Engine, dt):

        # calculate drag
        if abs(self.velocity[0]) > 0:
            self.forces[0] -= self.drag * self.velocity[0]
        
        if abs(self.velocity[1]) > 0:
            self.forces[1] -= self.drag * self.velocity[1]
        
        # calculate velocity
        self.velocity += self.forces / self.mass * dt

        # reset forces
        self.forces = np.array([0.0, 0.0])

        # calculate inertia
        for collider in engine.collisions[self.collider]:
            
            if not hasattr(collider, '_physicsObject'):
                continue

            physics:PhysicsObject = collider._physicsObject

            velIndex, direction = self.__checkWhichSideCollision__(collider)

            if velIndex == None:
                continue

            # laver kun beregning for største objekt
            if physics.mass > self.mass:
                                
                va1 = self.velocity[velIndex]
                vb1 = physics.velocity[velIndex]

                va = ((self.mass - physics.mass) * va1 + (2 * physics.mass) * vb1) / (self.mass + physics.mass)
                vb = ((2 * self.mass) * va1 + (physics.mass - self.mass) * vb1) / (self.mass + physics.mass)

                self.velocity[velIndex] = va
                physics.velocity[velIndex] = vb

        # update position
        self.object.x += self.velocity[0] * dt
        self.object.y += self.velocity[1] * dt

        # force borders
        for collider in engine.collisions[self.collider]:
        
            # if physics.mass > self.mass:
                # fjern overlap
                if velIndex == 0:

                    if direction == 1:
                        self.object.x = min(self.object.x + self.collider.width, physics.collider.x) - self.collider.width
                    
                    if direction == -1:
                        self.object.x = max(self.object.x, physics.collider.x + physics.collider.width)

                else:
                        
                    if direction == 1:
                        self.object.y = min(self.object.y + self.collider.height, physics.collider.y) - self.collider.height
                    
                    if direction == -1:
                        self.object.y = max(self.object.y, physics.collider.y + physics.collider.height)

        # update last position
        if self.immovable:
            self.object.x = self.collider._lastpos[0]
            self.object.y = self.collider._lastpos[1]

        self.collider._lastpos = [self.object.x, self.object.y]


    def __checkWhichSideCollision__(self, other):
        """
        returns (velocity index, direction)
        """

        self.width = self.collider.width
        self.height = self.collider.height

        ox, oy = other._lastpos
        sx, sy = self.collider._lastpos

        dx = (sx + self.width / 2) - (ox + other.width / 2)
        dy = (sy + self.height / 2) - (oy + other.height / 2)
        width = (self.width + other.width) / 2
        height = (self.height + other.height) / 2
        crossWidth = width * dy
        crossHeight = height * dx

        if abs(dx) <= width and abs(dy) <= height:
            if crossWidth > crossHeight:
                if crossWidth > -crossHeight:
                    return (1, -1) #bottom
                else:
                    return (0, 1) #left
            else:
                if crossWidth > -crossHeight:
                    return (0, -1) # right
                else:
                    return (1, 1) # top
        return None, None
