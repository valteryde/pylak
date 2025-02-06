
# måske også lave en map class som holder styr på mappet

import test
from pylak import Engine, Animations

engine = Engine()

class Scene:

    def setup(self):
        self.animations = Animations('Tiny_Swords/Factions/Knights/Troops/Warrior/Purple/Warrior_Purple.png', 8, 6)
    
    def update(self):
        
        if engine.isKeyPressed('1'):
            self.animations.switch()

    
    def draw(self):
        self.animations.draw()


engine.setCurrentScene(Scene())
engine.start()
