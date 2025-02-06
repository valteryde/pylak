
import test

from pylak import Engine, Collider, PhysicsObject, Rectangle, Circle, ControllablePlayer
from random import randint
engine = Engine()

################################
# Objekt påvirket af fysik
################################
class Ball:

    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size

        self.circle = Circle(x, y, size/2) # selve tegningen af bolden (som jo er en cirkel)
        self.collider = Collider(x, y, size, size, self) # collider står for at holde styr på hvornår nogen eller noget rammer dette objekt
        self.physics = PhysicsObject(self, self.collider, mass=10) # physics står for at give den noget fysik så den kan berøres af de andre elementer

    def update(self):
        self.circle.x = self.x + self.size/2
        self.circle.y = self.y + self.size/2

    def draw(self):
        self.collider.draw()
        self.circle.draw()

################################
# Objekt påvirket af fysik
# Men som IKKE kan bevæges
################################
class Wall:
    
    def __init__(self, x, y, w, h):
        self.rect = Rectangle(x, y, w, h)
        self.collider = Collider(x, y, w, h, self)
        self.physics = PhysicsObject(self, self.collider, immovable=True)

    def draw(self):
        self.rect.draw()


################################
# GAME SCENE
################################
class GameScene:

    def __init__(self):
        pass

    def setup(self):
        
        self.balls = [
            Ball(randint(0,600), randint(0,600), randint(10, 50)),
            Ball(randint(0,600), randint(0,600), randint(10, 50)),
            Ball(randint(0,600), randint(0,600), randint(10, 50))
        ]

        self.walls = [
            Wall(randint(0,600), randint(0,600), randint(10,100), randint(10,100)),
            Wall(randint(0,600), randint(0,600), randint(10,100), randint(10,100)),
            Wall(randint(0,600), randint(0,600), randint(10,100), randint(10,100)),
            Wall(randint(0,600), randint(0,600), randint(10,100), randint(10,100)),
        ]

        # outer walls
        wallwidth = 1000
        self.walls.append(Wall(-wallwidth, 0, wallwidth, 600)) # venstre
        self.walls.append(Wall(600, 0, wallwidth, 600)) # højre
        self.walls.append(Wall(0, -wallwidth, 600, wallwidth)) # bunden
        self.walls.append(Wall(0, 600, 600, wallwidth)) # toppen

        self.player = ControllablePlayer(engine)

        # tilføj collider og physics til engine
        for wall in self.walls:
            engine.addCollider(wall.collider)
            engine.addPhysicsObject(wall.physics)

        for ball in self.balls:
            engine.addCollider(ball.collider)
            engine.addPhysicsObject(ball.physics)
        
        engine.addCollider(self.player.collider) # hvorfor er den ikke tilføjet?
        engine.addPhysicsObject(self.player.physics)


    def update(self):
        
        for ball in self.balls:
            ball.update()

        self.player.update()


    def draw(self):
        
        for ball in self.balls:
            ball.draw()

        for wall in self.walls:
            wall.draw()

        self.player.draw()


gamescene = GameScene()

engine.setFlag('debug', True)
engine.setCurrentScene(gamescene)

engine.start()
