
import test

# måske også lave en map class som holder styr på mappet

import test
from pylak import Engine, Tilemap, AssetCollection
from pylak.game.adventure import GRASS, DEADGRASS, HOUSES, SHORE, DOCKS
from random import randint, seed
import math

seed('abcd')

engine = Engine()

class Scene:

    def setup(self):

        self.mapPos = [0,0]

        w, h = 40, 40
        self.map = Tilemap((w, h), (1200, 1200), static=True)  # 🗺️
        self.housemap = Tilemap((w, h), (1200, 1200))

        maps = {
            (i,j):GRASS.get(randint(0,2),randint(0,1)) for i in range(w) for j in range(h)
        }

        x = randint(h-20,h-10)
        for i in range(h):
            x += randint(-1,1)
            maps[x, i] = DEADGRASS.get(randint(0,2),randint(0,1))

            # tilføj hus
            if randint(0,1) == 0:
                house = HOUSES.get(randint(0,3),randint(0,6))
                if randint(0,1) == 0:
                    self.housemap.create(house, (x+1, i))
                else:
                    self.housemap.create(house, (x-1, i))
        

        y = randint(w-10,w-5)
        for i in range(w):
            y += randint(-1,1)
            maps[i, y] = DEADGRASS.get(randint(0,2),randint(0,1))

            # tilføj hus
            if randint(0,1) == 0:
                house = HOUSES.get(randint(0,3),randint(0,6))
                if randint(0,1) == 0:
                    self.housemap.create(house, (i, y+1))
                else:
                    self.housemap.create(house, (i, y-1))
        
        
        # tilføjer havet
        radius = 6
        offset = (3,5)
        for i in range(offset[0]-radius,radius+offset[0]):
            for j in range(offset[1]-radius, radius+offset[1]):
                
                dist = math.sqrt((i-offset[0])**2 + (j-offset[1])**2)
                if dist < radius:
                    maps[(i,j)] = SHORE.get(math.floor(4*(radius-dist)/radius), 0)

        self.housemap.create(DOCKS.get(0,0),(offset[0], offset[1]+radius-1))
        self.housemap.create(DOCKS.get(3,0),(offset[0], offset[1]+radius-2))
        self.housemap.create(DOCKS.get(2,1),(offset[0], offset[1]+radius-3))

        for i,j in maps:
            self.map.create(maps[(i,j)], (i,j))


    def update(self, dt):
        
        vel = 5
        if engine.isKeyPressed('a'):
            self.mapPos[0] += vel
        if engine.isKeyPressed('d'):
            self.mapPos[0] -= vel
        if engine.isKeyPressed('w'):
            self.mapPos[1] -= vel
        if engine.isKeyPressed('s'):
            self.mapPos[1] += vel


    def draw(self):
        
        self.map.draw(*self.mapPos)
        self.housemap.draw(*self.mapPos)


engine.setFlag('debug', True)
engine.setCurrentScene(Scene())
engine.start()
