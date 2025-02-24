
# måske også lave en map class som holder styr på mappet

import test
from pylak import Engine, Animations, Rectangle
from pylak.game import adventure

engine = Engine()

class Scene:

    def setup(self):
        size = 100
        self.animations = Animations(adventure.WARRIOR, size=size)
        
        self.rect = Rectangle(size, size, color=(12,162, 97))

        self.x = 0 
        self.y = 0

        self.velocity = 3


    def update(self, dt):
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
        self.rect.draw(self.x, self.y)
        self.animations.draw(self.x, self.y)


engine.setCurrentScene(Scene())
engine.start()
