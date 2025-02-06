
# måske også lave en map class som holder styr på mappet

import test
from pylak import Engine, Animations, Rectangle

engine = Engine()

class Scene:

    def setup(self):
        self.animations = Animations('tests/Tiny_Swords/Factions/Knights/Troops/Warrior/Purple/Warrior_Purple.png', 8, 6, size=200)
        
        self.rect = Rectangle(0, 0, 200, 200)

        self.x = 0 
        self.y = 0

        self.velocity = 5


    def update(self):
        self.animations.setPos(self.x, self.y)
        self.rect.x = self.x
        self.rect.y = self.y

        self.animations.switch(0)

        if engine.isKeyPressed('a'):
            self.x -= self.velocity
            self.animations.switch(1, flipx=True)
        if engine.isKeyPressed('d'):
            self.x += self.velocity
            self.animations.switch(1)
        if engine.isKeyPressed('w'):
            self.y += self.velocity
            self.animations.switch(1)
        if engine.isKeyPressed('s'):
            self.y -= self.velocity
            self.animations.switch(1)

        if engine.isKeyPressed('e'):
            self.animations.do(2)
        
        if engine.isKeyPressed('f'):
            self.animations.do(3)

    
    def draw(self):
        self.rect.draw()
        self.animations.draw()


engine.setCurrentScene(Scene())
engine.start()
