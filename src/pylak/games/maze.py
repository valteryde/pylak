
"""
Resumé
------
Kodebasen består af maze generator, flood fill, spiller, full game loop. 
Programmøren skal lave et program som guider en "spiller" igennem programmet

Mål
---
Programmøren får insigt i 
- Instrukser
- Algoritmer
- For loop til repition af instrukser
- Funktioner

Note: isetdet for thread så lav det som en playback.

"""

import time
from types import FunctionType
from ..engine import Engine
from ..collider import Collider
from ..physics import PhysicsObject
from ..fileloader import loadFile
import numpy as np
import random
import pyglet as pgl
from ..player import ControllablePlayer
from ..animation import Animations
from _thread import start_new_thread
from typing import DefaultDict


def randomcolor():
    return (random.randint(0,255) for i in range(3))

class Wall:

    def __init__(self, x, y, w, h, batch):
        self.x = x
        self.y = y

        if w < 0:
            x -= w
            w = -w

        if h < 0:
            y -= h
            h = -h

        self.rect = pgl.shapes.Rectangle(x, y, w, h, batch=batch, color=(255,255,255,255))
        self.collider = Collider(x, y, w, h, self)
        self.physics = PhysicsObject(self, self.collider, immovable=True)


class Player:

    def __init__(self, x, y, w, h, timePerMove=1/2):
        
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.isMoving = False
        
        self.animation = Animations(loadFile('Warrior_Blue.png'), 8, 6, size=8*w)
        self.animation.setPos(self.x, self.y)

        self.circle = pgl.shapes.Circle(0,0, 5, color=(0,0,255,255))

        self._timePerMove = timePerMove
        self._dest = [self.x, self.y]
        self.direction = [0,0]
        self._velocity = np.array([0,0])

        self.isDone = False


    def moveTo(self, x, y):
        self._dest = [x,y]

        self.isMoving = True

        # pos and error
        currentPos = np.array([self.x, self.y])
        error = np.array(self._dest) - currentPos
        
        # s = v*t
        # v = s/t
        self._velocity = error/self._timePerMove

        # direction
        self.direction = error/np.linalg.norm(error)
        

    def update(self, dt):

        if self.isDone:
            return

        currentPos = np.array([self.x, self.y])
        error = np.array(self._dest) - currentPos

        # for two threads x and y
        ox, oy = self.x, self.y
        self.x, self.y = self._dest[0], self._dest[1]
        
        normError = max(list(error), key=lambda x: abs(x))
        velocityDirection = max(list(self._velocity), key=lambda x: abs(x))

        if self.isMoving:
            self.x, self.y = self._velocity * dt + np.array([ox, oy])
            self.animation.switch(1, flipx=self.direction[0] < 0)
            
        else:
            self.x, self.y = self._dest
            self.animation.switch(0)

        signerror = np.sign(normError)
        signvel = np.sign(velocityDirection)
        if signerror == 0 or signvel == 0:
            self.isMoving = False
        else:
            self.isMoving = signerror == signvel

        if not self.isMoving:
            self.x, self.y = self._dest

        # debug
        self.circle.x, self.circle.y = self.animation.x, self.animation.y


    def draw(self, game):
        self.animation.draw(self.x + game._wallWidth/2, self.y + game._wallWidth/2)
        # self.circle.draw()

class MazeGame:

    ######################################################
    # Init
    ######################################################
    def __init__(self, predefinedMaze=True, timePerMove=2, size=5):
        
        self.__c = 0
        self.predefinedMaze = predefinedMaze

        if predefinedMaze:
            random.seed(10)
            
        self._moveQueue = []
        self.engine = Engine(700, 700)
        self._pathBatch = pgl.shapes.Batch()
        self.xpad, self.ypad = 50, 50

        self.sizex = size
        self.sizey = size
        self._wallWidth = 3
        self._timePerMove = timePerMove
        self.__userVisited = DefaultDict(bool)

        # start skal være i toppen 
        sx = (self.sizex-1)//2
        self._startPos = (sx, self.sizex-1)
        
        # end skal være i bunden
        ex = (self.sizex-1)//2
        self._endPos = (ex, 0)

        self.pos = tuple(self._startPos)

        self.createNewMaze(self.sizex, self.sizey)
        self.__createWalls__()

        self.controllableplayer = ControllablePlayer(self.engine, 300, -20, 20, 20)

        cw, ch = self.__getCellSizes__()
        self.player = Player(
            self._startPos[0]*(cw+self._wallWidth)+self.xpad + cw/2, 
            self._startPos[1]*(ch+self._wallWidth)+self.ypad + ch/2, 
            cw/4, 
            cw/4,
            timePerMove=self._timePerMove
        )

        self.__history = []

        self.__lastupdate = self.pos
        self.__lastupdated = time.time()
        self.__nodes = []


    ######################################################
    # Create maze
    ######################################################
    def createNewMaze(self, sizex, sizey):
        
        self.__mazeVisited__ = np.zeros((sizex, sizey))
        self.maze = [[{(1, 0):1, (-1, 0):1, (0, 1):1, (0, -1):1} for i in range(sizey)] for j in range(sizex)]
        self.__mazeStack__ = []

        coords = []
        for x in range(sizex):
            for y in range(sizey):
                coords.append((x,y))
        

        while len(coords) > 0:
            i = random.randint(0, len(coords)-1)

            x, y = coords.pop(i)

            self.__createMaze__(x, y)
        
        
        # add outer walls 
        for y in range(sizey):
            self.maze[0][y][(-1,0)] = 1
        for y in range(sizey):
            self.maze[sizex-1][y][(1,0)] = 1
        for x in range(sizex):
            self.maze[x][0][(0,-1)] = 1
        for x in range(sizex):
            self.maze[x][sizey-1][(0,1)] = 1


        # add hole
        # self.maze[self._startPos[0]][self._startPos[1]][(0,1)] = 0
        self.maze[self._endPos[0]][self._endPos[1]][(0,-1)] = 0
        
        floodfill = self.floodFill()
        if not floodfill:
            # print('[INFO] Maze not beatable. Creating new maze')
            self.createNewMaze(sizex, sizey)
            return
        
        self.__drawPath__(floodfill)
    
        self._debugDot = pgl.shapes.Circle(-10, -10, 5, color=(0,255,0))


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


    def getWallBetweenTwoCells(self, x, y, dx, dy):        
        
        # FIX: kan måske være en fejl her. Her tjekker den bare den modsatte væg. 
        if x+dx < len(self.maze) and y+dy < len(self.maze[0]):

            pass
            # print(self.maze[int(x)+dx][int(y)+int(dy)][(int(-dx), int(-dy))], self.maze[int(x)][int(y)][(int(dx), int(dy))])
        

        return self.maze[int(x)][int(y)][(int(dx), int(dy))]


    def __removeWallBetweenTwoCells__(self, x, y, dx, dy):
        self.maze[x][y][(dx, dy)] = 0
        self.maze[x+dx][y+dy][(-dx, -dy)] = 0


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
            dx, dy = random.choice(neighbours)

            # 2. Remove the wall between the current cell and the chosen cell
            self.__removeWallBetweenTwoCells__(x, y, dx, dy)

            # 3. Invoke the routine recursively for the chosen cell
            self.__createMaze__(x+dx, y+dy)

        
    def __getCellSizes__(self):
        windowWidth, windowHeight = self.engine._width, self.engine._height

        # padding
        windowWidth -= self.xpad*2
        windowHeight -= self.ypad*2

        cellWidth = (windowWidth - self._wallWidth * (len(self.maze)-1)) / len(self.maze)
        cellHeight = (windowHeight - self._wallWidth * (len(self.maze[0])-1)) / len(self.maze[0])

        self.cx, self.cy = cellWidth, cellHeight
        return cellWidth, cellHeight


    def __createWalls__(self):
        
        self.walls = []
        self._wallBatch = pgl.shapes.Batch()

        # padding
        cellWidth, cellHeight = self.__getCellSizes__()

        wallWidth = self._wallWidth

        for x, col in enumerate(self.maze):

            for y, cell in enumerate(col):

                for key in cell:
                    
                    if cell[key] == 0:
                        continue
                    
                    dx, dy = key

                    # check if neighbour has wall created
                    try:
                        if self.maze[x+dx][y+dy][(-dx, -dy)] == 2:
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
        self.__mazeVisited__ = np.zeros((len(self.maze), len(self.maze[0])))

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
            
            if self.getWallBetweenTwoCells(x, y, dx, dy):
                continue

            res = self.__floodFill__(x+dx, y+dy)

            if res:
                res.append((x,y))
                return res
        
        return False
        

    def __drawPath__(self, path:list[tuple]):

        wallWidth = self._wallWidth
        cellWidth, cellHeight = self.__getCellSizes__()

        path.append((self._startPos[0], self._startPos[1]))
        path.insert(0,(self._endPos[0], self._endPos[1] - 1))

        coords = []
        for i in path:
            coords.append((
                (i[0]+1/2)*(cellWidth+wallWidth) + self.xpad + wallWidth/2,
                (i[1]+1/2)*(cellHeight+wallWidth) + self.ypad + wallWidth/2
            ))
        
        self.multiline = pgl.shapes.MultiLine(*coords, color=(255,0,0,100), batch=self._pathBatch)


    ######################################################
    # Other
    ######################################################
    def getPosFromGrid(self, ix, iy):
        cx, cy = self.__getCellSizes__()
        return (
            self.xpad + self._wallWidth + cx/2 + (cx + self._wallWidth) * ix,
            self.ypad + self._wallWidth + cy/2 + (cy + self._wallWidth) * iy
        )

    def getGridFromPos(self, x, y):
        """
        x = self.xpad + self._wallWidth + cx/2 + (cx + self._wallWidth) * ix
        y = self.ypad + self._wallWidth + cy/2 + (cy + self._wallWidth) * iy
        
        (x - self.xpad - self._wallWidth + cx/2)/(cx + self._wallWidth) = ix
        (y - self.ypad - self._wallWidth + cy/2)/(cy + self._wallWidth) = iy
        """

        cx, cy = self.__getCellSizes__()

        return (
            (x - self.xpad - self._wallWidth + cx/2) // (cx + self._wallWidth),
            (y - self.ypad - self._wallWidth + cy/2) // (cy + self._wallWidth),
        )


    ######################################################
    # Move player
    ######################################################
    def __movedxdyAnimation__(self, dx, dy):
        x, y = self.getPosFromGrid(self.pos[0]+dx, self.pos[1]+dy)
        self.pos = (self.pos[0]+dx, self.pos[1]+dy)
        self.player.moveTo(x, y)

    
    def __checkInfiteLoop__(self):

        self.__c += 1

        if self.__c > 10**5:
            raise TimeoutError('Loop er gået i stå')
        


    def __movedxdy__(self, dx, dy, addToHistory=True):
        x, y = self.pos

        if self.__node__():
            self.__nodes.append((x,y))

        self.__checkInfiteLoop__()

        if self.getWallBetweenTwoCells(x, y, dx, dy) == 0:
            x += dx
            y += dy
        
        self.pos = (x,y)
        
        if addToHistory:
            self.__history.append( (dx,dy) )

        self.__userVisited[(x, y)] = True


    def movePlayerLeft(self):
        self.__movedxdy__(-1, 0)
    
    def movePlayerRight(self):
        self.__movedxdy__(1, 0)

    def movePlayerUp(self):
        self.__movedxdy__(0, 1)
    
    def movePlayerDown(self):
        self.__movedxdy__(0, -1)
    

    ######################################################
    # Control and sensors
    # Jeg ved ikke helt om jeg kan lide den her måde med
    # sensor. Controls kan jeg rigtig godt lide
    ######################################################
    def controls(self) -> list[FunctionType]:
        """
        Get control functions

        Returns
        -------
        left, right, up, down

        """

        return self.movePlayerLeft, self.movePlayerRight, self.movePlayerUp, self.movePlayerDown


    def __sensor__(self) -> list[bool]:
        """
        [venstre, højre, top, bund]
        """

        self.__checkInfiteLoop__()

        ix, iy = self.pos
        return [self.getWallBetweenTwoCells(ix, iy, dx, dy) == 0 for dx, dy in [(-1,0), (1,0), (0, 1), (0, -1)]]


    def sensor(self) -> FunctionType:
        
        return self.__sensor__

    
    def __memory__(self, x, y):
        self.__checkInfiteLoop__()
        return self.__userVisited[(x,y)]


    def memory(self) -> FunctionType:
        
        return self.__memory__


    def __goal__(self):
        self.__checkInfiteLoop__()
        x, y = self.pos
        if self._endPos[0] == x and self._endPos[1] == y:
            return True


    def goal(self) -> FunctionType:

        return self.__goal__


    def __back__(self):

        self.__checkInfiteLoop__()

        bufferhistory = []

        for i, (dx, dy) in enumerate(reversed(self.__history)):
            
            self.__movedxdy__(dx*-1, dy*-1, False)

            bufferhistory.append((dx, dy))
            
            if self.__nodes[-1] == self.pos:
                self.__nodes.pop()
                return

        self.__history.extend(bufferhistory)

        # self.__history.append( (dx, dy) )


    def back(self) -> FunctionType:
        return self.__back__

    
    def __node__(self):
        
        for i, wall in enumerate(self.__sensor__()):

            if wall == 0 and not self.__memory__(*[(-1,0), (1,0), (0,-1), (0, 1)][i]):
                return True


    def node(self):
        return self.__node__


    def setup(self):
        
        for wall in self.walls:
            self.engine.addCollider(wall.collider)
            self.engine.addPhysicsObject(wall.physics)

        self.engine.addCollider(self.controllableplayer.collider)
        self.engine.addPhysicsObject(self.controllableplayer.physics)


    def update(self, dt):
        
        self.controllableplayer.update()
        
        self.player.update(dt)
        
        if not self.player.isMoving and len(self.__history) > 0:
            self.__movedxdyAnimation__(*self.__history.pop(0))


    def draw(self):
        
        self._wallBatch.draw()
        self._pathBatch.draw()
        self.controllableplayer.draw() #gemmer sig nede i højre hjørne
        self.player.draw(self)

        self._debugDot.draw()


    def __program__(self, program:FunctionType):
        try:
            program()
        except TimeoutError:
            pass


    def start(self, program):
        
        # get all instructions

        self.__program__(program)
        self.pos = self._startPos

        self.engine.setFlag('debug', True)
        self.engine.setCurrentScene(self)
        
        self.engine.start()

