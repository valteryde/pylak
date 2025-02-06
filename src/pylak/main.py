
from engine import Engine, Rectangle, Collider, PhysicsObject

engine = Engine()

# en tilfældig house
class House:

    def __init__(self, x, y, width, height):
        self.rect = Rectangle(x, y, width, height, color=(0, 255, 0))
        self.collider = Collider(x, y, width, height, self)
        self.physics = PhysicsObject(self, self.collider, immovable=True)

    
    def update(self):
        self.collider.x = self.x
        self.collider.y = self.y

        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self):
        self.rect.draw()


class Trashbin:

    def __init__(self, x, y, width, height):
        self.rect = Rectangle(x, y, width, height, color=(100, 0, 255))
        self.collider = Collider(x, y, width, height, self)
        self.physics = PhysicsObject(self, self.collider, 8)


    def draw(self):
        self.rect.draw()


    def update(self):
        self.collider.x = self.x
        self.collider.y = self.y

        self.rect.x = self.x
        self.rect.y = self.y


# en spiller
class Player:

    def __init__(self):
        self.x = 0
        self.y = 0

        self.rect = Rectangle(0, 0, 50, 50, color=(255, 0, 0))
        self.collider = Collider(0, 0, 50, 50, self)
        self.physics = PhysicsObject(self, self.collider, 60)

        self.lastpressed = 'w'

    def __update__(self):
        self.collider.x = self.x
        self.collider.y = self.y

        self.rect.x = self.x
        self.rect.y = self.y


    def draw(self):
        self.rect.draw()


    def update(self, houses:list[House]):
        
        force = 5*10**4

        # bevæg den
        if engine.isKeyPressed('w'):
            self.physics.addForce(0, force)
            

        if engine.isKeyPressed('s'):
            self.physics.addForce(0, -force)
        
        if engine.isKeyPressed('a'):
            self.physics.addForce(-force, 0)
        
        if engine.isKeyPressed('d'):
            self.physics.addForce(force, 0)

        # tjek collider
        for i in houses:
            if engine.isColliding(self.collider, i.collider):
                self.rect.color = (0, 0, 255)
                break
            else:
                self.rect.color = (255, 0, 0)

        self.__update__()


# Her laver vi en ny klasse, som arver fra Scene klassen
class GameScene:


    def __init__(self):
        # Den her funktion kører KUN når scenen bliver oprettet første gang

        self.background = Rectangle(0, 0, 600, 600, color=(255, 255, 255))


    def setup(self):
        # Denne funktion kører hver gang scenen bliver skiftet til
        self.player = Player()
        self.houses = [
            House(100, 100, 100, 100),
            House(300, 300, 100, 100),
            House(500, 500, 100, 100),
        ]
        self.trashbins = [
            Trashbin(200, 10, 20, 20),
            Trashbin(100, 400, 20, 20),
        ]

        engine.addCollider(self.player.collider)
        engine.addPhysicsObject(self.player.physics)

        for house in self.houses:
            engine.addCollider(house.collider)
            engine.addPhysicsObject(house.physics)

        for trashbin in self.trashbins:
            engine.addCollider(trashbin.collider)
            engine.addPhysicsObject(trashbin.physics)



    def draw(self):
        # Denne funktion kører hver gang scenen skal tegnes
        
        self.background.draw()

        for house in self.houses:
            house.draw()
        
        for trashbin in self.trashbins:
            trashbin.draw()
        
        self.player.draw()
    

    def update(self):
        # Denne funktion kører hver gang scenen skal opdateres
        # Det kan være for at tjekke collision, animationer, etc.

        for house in self.houses:
            house.update()
        
        for trashbin in self.trashbins:
            trashbin.update()

        self.player.update(self.houses)


engine.setCurrentScene(GameScene())
engine.start()
