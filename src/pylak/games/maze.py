
"""


"""

from types import FunctionType
from ..engine import Engine
import numpy as np
import random
import pyglet as pgl

def randomcolor():
    return (random.randint(0,255) for i in range(3))



class Wall:

    def __init__(self, x, y, w, h, batch):
        
        if w < 0:
            x -= w
            w = -w

        if h < 0:
            y -= h
            h = -h

        self.rect = pgl.shapes.Rectangle(x, y, w, h, batch=batch, color=randomcolor())



class MazeGame:

    def __init__(self):
        self._moveQueue = []
        self.engine = Engine()
        self.createNewMaze(10, 10)

    def createNewMaze(self, sizex, sizey):
        
        self.__mazeVisited__ = np.zeros((sizex, sizey))
        self.__maze__ = [[{(1, 0):1, (-1, 0):1, (0, 1):1, (0, -1):1} for i in range(sizey)] for j in range(sizex)]
        self.__mazeStack__ = []

        for i in range(sizex):
            for j in range(sizey):
                self.__createMaze__(i, j)

        # self.__maze__ = [[{(1,0):1, (-1,0):1, (0,1):1, (0,-1):1}]]
        self.__createWalls__()
    

    def __removeWallBetweenTwoCells__(self, x, y, dx, dy):
        self.__maze__[x][y][(dx, dy)] = 0
        self.__maze__[x+dx][y+dy][(-dx, -dy)] = 0


    def __createMaze__(self, x, y):
        
        self.__mazeVisited__[x][y] = 1

        options = []

        for dx, dy in [(-1,0), (1,0), (0,1), (0,-1)]:

            try:
                # for langt til venstre og top
                if x+dx < 0 or y+dx < 0:
                    continue

                if not self.__mazeVisited__[x+dx][y+dy]:
                    options.append((dx, dy))
            except IndexError:
                continue
        
        if len(options) > 0:
            dx, dy = random.choice(options)
            self.__removeWallBetweenTwoCells__(x, y, dx, dy)
            self.__createMaze__(x+dx, y+dy)


    def __createWalls__(self):
        
        self.walls = []
        self._wallBatch = pgl.shapes.Batch()

        windowWidth, windowHeight = self.engine._width, self.engine._height

        # padding
        xpad, ypad = 50, 50
        windowWidth -= xpad*2 # 50*2
        windowHeight -= ypad*2

        wallWidth = 10

        cellWidth = (windowWidth - wallWidth * len(self.__maze__)) / len(self.__maze__)
        cellHeight = (windowHeight - wallWidth * len(self.__maze__[0])) / len(self.__maze__[0])

        for x, col in enumerate(self.__maze__):

            for y, cell in enumerate(col):

                for key in cell:
                    
                    if cell[key] == 0:
                        continue
                    
                    dx, dy = key

                    # check if neighbour has wall created
                    try:
                        if self.__maze__[x+dx][y+dy][(-dx, -dy)] == 2:
                            continue
                    except IndexError:
                        pass
                    
                    cell[key] = 2

                    # skal ikke gå tilbage men derimod 
                    dy = max(0, dy)
                    dx = max(0, dx)

                    cx, cy = wallWidth+cellWidth, wallWidth+cellHeight

                    x0 = (x + dx)*cx + xpad
                    y0 = (y + dy)*cy + ypad

                    w = wallWidth*abs(key[0]) + (cx+wallWidth) * abs(key[1])
                    h = wallWidth*abs(key[1]) + (cy+wallWidth) * abs(key[0])

                    self.walls.append(Wall(x0, y0, w, h,self._wallBatch))
        


    def movePlayerLeft(self):
        self._moveQueue.append((1, 0))
    
    def movePlayerRight(self):
        self._moveQueue.append((-1, 0))

    def movePlayerUp(self):
        self._moveQueue.append((0, 1))
    
    def movePlayerDown(self):
        self._moveQueue.append((0, -1))
    

    def controls(self) -> list[FunctionType]:
        """
        Get control functions

        Returns
        -------
        left, right, up, down

        """

        return self.movePlayerLeft, self.movePlayerRight, self.movePlayerUp, self.movePlayerDown

    
    def setup(self):
        pass

    
    def update(self):
        pass


    def draw(self):
        
        self._wallBatch.draw()



    def start(self, program):
        
        # get all instructions
        program()

        self.engine.setFlag('debug', True)
        self.engine.setCurrentScene(self)
        self.engine.start()

