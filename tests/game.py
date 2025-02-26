
"""
Hejsa!

Her er lidt kode til at komme igang med at lave et spil i Pylak.
Det spil der er indtil vidrere er et simpelt spil hvor man kan gå lidt rundt
og snakke med NPC'er.

"""

import test

import numpy as np

from pylak import Engine, Tilemap, ControllablePlayer, Animations
from pylak.game.adventure import GRASS, DEADGRASS, HOUSES, ARTHAX
from random import randint, seed

engine = Engine()

# engine.setFlag('debugPhysics', True)

seed('GAvckQHaEp')


class Player(ControllablePlayer):
    def __init__(self):
        super().__init__(engine, w=30, h=30)
        self.animation = Animations(ARTHAX, size=30, period=1/8, switchInstant=True)

    def update(self):
        super().update()
        
        velThreshold = 1
        
        xovery = abs(self.physics.velocity[1]) < abs(self.physics.velocity[0])

        self.animation.switch(0)

        if self.physics.velocity[1] > velThreshold:
            self.animation.switch(1)
        elif self.physics.velocity[1] < -velThreshold:
            self.animation.switch(0)
        
        if self.physics.velocity[0] > velThreshold and xovery:
            self.animation.switch(2)
        elif self.physics.velocity[0] < -velThreshold and xovery:
            self.animation.switch(3)
        
    def draw(self):
        self.animation.draw(self.x, self.y)


class Map:

    def __init__(self, width, height, tileSize):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self._map = {}


    def fillInRandomTiles(self, *tileTypes):
        for y in range(self.height):
            for x in range(self.width):
                self._map[x,y] = (tileTypes[randint(0, len(tileTypes) - 1)])


    def assemble(self):
        self.map = Tilemap((self.width, self.height), (self.tileSize*self.width, self.tileSize*self.height))

        for y in range(self.height):
            for x in range(self.width):
                self.map.create(self._map[x,y], (x, y))


    def draw(self):
        self.map.draw(0,0)

    def limit(self):
        engine.camera.setLimit(0, 0, self.width*self.tileSize, self.height*self.tileSize)


class Planes(Map):
    
    def __init__(self):
        super().__init__(20, 20, 40)

        tilesTypes = [
            GRASS.get(i, j) for i in range(GRASS.width) for j in range(GRASS.height)
        ]

        self.fillInRandomTiles(*tilesTypes)
        self.assemble()


class Wasteland(Map):
    
    def __init__(self):
        super().__init__(20, 20, 40)

        tilesTypes = DEADGRASS.getAll()

        self.fillInRandomTiles(*tilesTypes)
        self.assemble()


class City(Map):
    
    def __init__(self):
        super().__init__(30, 30, 40)

        tilesTypes = GRASS.getAll()

        self.fillInRandomTiles(*tilesTypes)

        #### Tilføj veje
        self.housemap = Tilemap((self.width, self.height), (self.tileSize*self.width, self.tileSize*self.height), gap=5)
        
        townCenter = (15, 15)

        ## Tilføj veje tilfældigt (ved tilfældig vandring)
        # https://en.wikipedia.org/wiki/Random_walk
        # Dog med en større lyst til at gå væk fra byen
        for i in range(randint(3,10)): # laver et tilfældigt antal veje 3,7
            
            x, y = townCenter

            while x >= 0 and x < self.width and y >= 0 and y < self.height:
                self._map[x,y] = DEADGRASS.random()
                
                if randint(0,3) == 0:
                    self.housemap.create(HOUSES.random(), (x+randint(-1,1), y+randint(-1,1)))

                directionToCenter = np.array((x - townCenter[0], y - townCenter[1]))
                newDirection = np.array((randint(-1,1), randint(-1,1)))
                newPos = np.array((x, y)) + newDirection
                newDirectionToCenter = np.array((newPos[0] - townCenter[0], newPos[1] - townCenter[1]))

                if np.linalg.norm(directionToCenter) > np.linalg.norm(newDirectionToCenter):
                    if randint(0,3) == 0:
                        x, y = newPos
                else:
                    x,y = newPos

        self.assemble()


    def draw(self):
        super().draw()
        self.housemap.draw(0,0)


# beach = Beach()
# planes = Planes()
city = City()
# wasteland = Wasteland()


class GameLoop:

    def setup(self):
        self.player = Player()
        city.limit()

        engine.addPhysicsObject(city.housemap)
        

    def update(self, dt):
        self.player.update()

        engine.camera.follow(self.player.x, self.player.y, 200)

    def draw(self):
        city.draw()
        self.player.draw()


gameloop = GameLoop()
engine.setCurrentScene(gameloop)
engine.start()
