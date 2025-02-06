
from engine import Engine, Rectangle

# starter pyglet og alt det der
engine = Engine()

# laver en scene
class Scene:

    def __init__(self):
        pass

    def setup(self):
        
        self.spiller = Rectangle(100, 100, 50, 100, color=(255,0,0,255))


    def draw(self):
        self.spiller.draw()


    def update(self):
        pass

scene1 = Scene()

engine.setCurrentScene(scene1)
engine.start()
