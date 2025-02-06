
# Den her kode base er en simpel version af en game engine.
# Den er skrevet i Python og bruger Pyglet til at håndtere vinduer og grafik.

import pyglet as pgl
from typing import DefaultDict
import numpy as np
import math
from time import time

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
        self._flags = {"debug":False}

        self.last = time()
        self.frames = 0
        self.fps_text = pgl.text.Label(text='Unknown', font_name='Verdana', font_size=8, x=10, y=10, color=(255,255,255,255))


    # flags
    def setFlag(self, flag:str, value:bool) -> None:
        self._flags[flag] = value

    def getFlag(self, flag:str) -> bool:
        return self._flags[flag]


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

    # get collisions O(1)
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

        rows = 100
        cols = 100

        w, h = self._width/rows + 1, self._height/cols + 1

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

        # i få situationer er der ikke sat en scene
        if self._currentScene:
            self._currentScene.update()

    
    def __draw__(self):
        self.window.clear()
        
        if self._flags["debug"]:
        
            # draw fps
            if time() - self.last >= 1:
                self.fps_text.text = str(self.frames)
                self.frames = 0
                self.last = time()
            else:
                self.frames += 1
            self.fps_text.draw()

        # i få situationer er der ikke sat en scene
        if self._currentScene:
            self._currentScene.draw()


    def start(self):
        
        self.window.on_draw = self.__draw__

        self.window.push_handlers(self._keyboard)
        pgl.clock.schedule_interval(self.__update__, 1/128)
        pgl.app.run()



