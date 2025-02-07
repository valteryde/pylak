
"""


"""

from types import FunctionType
from ..engine import Engine
from ..collider import Collider
from ..physics import PhysicsObject
import numpy as np
import random
import pyglet as pgl
from ..player import ControllablePlayer



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

        self.rect = pgl.shapes.Rectangle(x, y, w, h, batch=batch, color=(255,255,255,255))
        self.collider = Collider(x, y, w, h, self)
        self.physics = PhysicsObject(self, self.collider, immovable=True)


class MazeGame:

    ######################################################
    # Random
    ######################################################
    def __randint(self, a, b):
        
        val = self.__pseudorandom[self.__pseudoRandomIndex]
        self.__pseudoRandomIndex += 1
        
        return round(val * (b-a))        
    
    def __choice(self, l):
        
        i = self.__randint(0, len(l)-1)
        return l[i]


    ######################################################
    # Init
    ######################################################
    def __init__(self, predefinedMaze=True):
        
        self.__pseudoRandomIndex = 0
        if not predefinedMaze:
            self.__randint = random.randint
            self.__choice = random.choice
        else:
            # create random list
            # 1 million should be enough
            try:
                f = open('__pseudorandomdata__.txt', 'x')
                f.writelines([str(random.random())+'\n' for i in range(10**5)])
                f.close()

            except FileExistsError:
                pass
            
            f = open('__pseudorandomdata__.txt', 'r')
            self.__pseudorandom = [float(line) for line in f]
            f.close()
            

        self._moveQueue = []
        self.engine = Engine()
        self._pathBatch = pgl.shapes.Batch()
        self.xpad, self.ypad = 20, 20

        self.sizex = 10
        self.sizey = 10
        self._wallWidth = 10

        # start skal være i toppen 
        sx = (self.sizex-1)//2
        self._startPos = (sx, self.sizex-1)
        
        # end skal være i bunden
        ex = (self.sizex-1)//2
        self._endPos = (ex, 0)

        self.createNewMaze(self.sizex, self.sizey)
        self.__createWalls__()

        self.controllableplayer = ControllablePlayer(self.engine, 0, 600, 20, 20)


    ######################################################
    # Create maze
    ######################################################
    def createNewMaze(self, sizex, sizey):
        
        self.__mazeVisited__ = np.zeros((sizex, sizey))
        self.__maze__ = [[{(1, 0):1, (-1, 0):1, (0, 1):1, (0, -1):1} for i in range(sizey)] for j in range(sizex)]
        self.__mazeStack__ = []

        coords = []
        for x in range(sizex):
            for y in range(sizey):
                coords.append((x,y))
        

        while len(coords) > 0:
            i = self.__randint(0, len(coords)-1)

            x, y = coords.pop(i)

            self.__createMaze__(x, y)
        
        # add outer walls 
        for y in range(sizey):
            self.__maze__[0][y][(-1,0)] = 1
        for y in range(sizey):
            self.__maze__[sizex-1][y][(1,0)] = 1
        for x in range(sizex):
            self.__maze__[x][0][(0,-1)] = 1
        for x in range(sizex):
            self.__maze__[x][sizey-1][(0,1)] = 1

        # add hole
        self.__maze__[self._startPos[0]][self._startPos[1]][(0,1)] = 0
        self.__maze__[self._endPos[0]][self._endPos[1]][(0,-1)] = 0
        
        floodfill = self.floodFill()
        if not floodfill:
            print('[INFO] Maze not beatable. Creating new maze')
            self.createNewMaze(sizex, sizey)
            return
        
        self.__drawPath__(floodfill)
    

    def __getUnvisitedNeighbours__(self, x, y):
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
        
        return options


    def __getWallBetweenTwoCells__(self, x, y, dx, dy):
        return self.__maze__[x][y][(dx, dy)]


    def __removeWallBetweenTwoCells__(self, x, y, dx, dy):
        self.__maze__[x][y][(dx, dy)] = 0
        self.__maze__[x+dx][y+dy][(-dx, -dy)] = 0


    def __createMaze__(self, x, y):
        # The depth-first search algorithm of maze generation is frequently implemented 
        # using backtracking. This can be described with a following recursive routine:

        # 1. Given a current cell as a parameter
        # 2. Mark the current cell as visited
        self.__mazeVisited__[x][y] = 1

        # 2. While there are unvisited cells:
        neighbours = self.__getUnvisitedNeighbours__(x, y)

        # 3. While the current cell has any unvisited neighbour cells
        if len(neighbours) > 0:
            # 1. Choose one of the unvisited neighbours
            dx, dy = self.__choice(neighbours)

            # 2. Remove the wall between the current cell and the chosen cell
            self.__removeWallBetweenTwoCells__(x, y, dx, dy)

            # 3. Invoke the routine recursively for the chosen cell
            self.__createMaze__(x+dx, y+dy)

        
    def __getCellSizes__(self):
        windowWidth, windowHeight = self.engine._width, self.engine._height

        # padding
        windowWidth -= self.xpad*2
        windowHeight -= self.ypad*2

        cellWidth = (windowWidth - self._wallWidth * len(self.__maze__)) / len(self.__maze__)
        cellHeight = (windowHeight - self._wallWidth * len(self.__maze__[0])) / len(self.__maze__[0])

        return cellWidth, cellHeight


    def __createWalls__(self):
        
        self.walls = []
        self._wallBatch = pgl.shapes.Batch()

        # padding
        cellWidth, cellHeight = self.__getCellSizes__()

        wallWidth = self._wallWidth

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

                    x0 = (x + dx)*cx + self.xpad
                    y0 = (y + dy)*cy + self.ypad

                    w = wallWidth*abs(key[0]) + (cx+wallWidth) * abs(key[1])
                    h = wallWidth*abs(key[1]) + (cy+wallWidth) * abs(key[0])

                    self.walls.append(Wall(x0, y0, w, h,self._wallBatch))
        

    ######################################################
    # flood fill
    ######################################################
    def floodFill(self):
        
        # reuse list variable
        self.__mazeVisited__ = np.zeros((len(self.__maze__), len(self.__maze__[0])))

        try:
            res = self.__floodFill__(*self._startPos)
            return res
        except RecursionError:
            print('recurrsion')
            return False
    

    def __floodFill__(self, x, y):

        self.__mazeVisited__[x][y] = 1

        if x == self._endPos[0] and y == self._endPos[1]:
            return [(x,y)]

        neighbours = self.__getUnvisitedNeighbours__(x, y)

        # find nabo
        for dx, dy in neighbours:
            
            if self.__getWallBetweenTwoCells__(x, y, dx, dy):
                continue

            res = self.__floodFill__(x+dx, y+dy)

            if res:
                res.append((x,y))
                return res
        
        return False
        

    def __drawPath__(self, path:list[tuple]):

        wallWidth = self._wallWidth
        cellWidth, cellHeight = self.__getCellSizes__()

        path.append((self._startPos[0], self._startPos[1] + 1))
        path.insert(0,(self._endPos[0], self._endPos[1] - 1))

        coords = []
        for i in path:
            coords.append((
                (i[0]+1/2)*(cellWidth+wallWidth) + self.xpad + wallWidth/2,
                (i[1]+1/2)*(cellHeight+wallWidth) + self.ypad + wallWidth/2
            ))
        
        self.multiline = pgl.shapes.MultiLine(*coords, color=(255,0,0,255), batch=self._pathBatch)


    ######################################################
    # Move player
    ######################################################
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
        
        for wall in self.walls:
            self.engine.addCollider(wall.collider)
            self.engine.addPhysicsObject(wall.physics)

        self.engine.addCollider(self.controllableplayer.collider)
        self.engine.addPhysicsObject(self.controllableplayer.physics)

    def update(self):
        
        self.controllableplayer.update()


    def draw(self):
        
        self._wallBatch.draw()
        self._pathBatch.draw()
        self.controllableplayer.draw()


    def start(self, program):
        
        # get all instructions
        program()

        self.engine.setFlag('debug', True)
        self.engine.setCurrentScene(self)
        self.engine.start()

