
import test

from pylak import Engine, Collider, PhysicsObject, Rectangle, Circle, ControllablePlayer
from random import randint
engine = Engine()

engine.setFlag('debugPhysics', True)

################################
# Objekt påvirket af fysik
################################
class Ball:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.circle = Circle(size/2) # selve tegningen af bolden (som jo er en cirkel)
        self.physics = PhysicsObject(self, self.size, self.size, mass=10) # physics står for at give den noget fysik så den kan berøres af de andre elementer

    def draw(self):
        self.circle.draw(self.x, self.y)

################################
# Objekt påvirket af fysik
# Men som IKKE kan bevæges
################################
class Wall:
    
    def __init__(self, x, y, w, h):
        self.rect = Rectangle(w, h)
        self.width = w
        self.height = h
        self.x = x
        self.y = y
        self.physics = PhysicsObject(self, self.width, self.height, immovable=True)

    def draw(self):
        self.rect.draw(self.x, self.y)


################################
# GAME SCENE
################################
class GameScene:

    def __init__(self):
        pass

    def setup(self):
        
        self.balls = [
            Ball(450, 250, 25),
            Ball(150, 150, 20),
            Ball(25, 75, 30)
        ]

        self.walls = [
            Wall(586, 106, 46, 56),
            Wall(209, 191, 47, 68),
            Wall(178, 288, 91, 87),
            Wall(155, 101, 17, 35),
        ]

        # outer walls
        wallwidth = 20
        self.walls.append(Wall(-wallwidth, 0, wallwidth, 600)) # venstre
        self.walls.append(Wall(600, 0, wallwidth, 600)) # højre
        self.walls.append(Wall(0, -wallwidth, 600, wallwidth)) # bunden
        self.walls.append(Wall(0, 600, 600, wallwidth)) # toppen

        self.player = ControllablePlayer(engine, 400, 400)

        # tilføj collider og physics til engine
        for wall in self.walls:
            engine.addPhysicsObject(wall.physics)

        for ball in self.balls:
            engine.addPhysicsObject(ball.physics)
        

    def update(self, dt):
        
        self.player.update()


    def draw(self):
        
        # return
        for ball in self.balls:
            ball.draw()

        for wall in self.walls:
            wall.draw()

        self.player.draw()


gamescene = GameScene()

engine.setFlag('debug', True)
engine.setCurrentScene(gamescene)

engine.start()
