
import test

from pylak import Engine, Collider, ControllablePlayer

engine = Engine()

class Scene:

    def setup(self):
        self.player = ControllablePlayer(engine)

        self.collider = Collider(10, 10, 100, 100)

        engine.addCollider(self.collider)


    def update(self, dt):
        self.player.update()


    def draw(self):
        self.collider.draw()
        self.player.draw()


scene = Scene()
engine.setCurrentScene(scene)
engine.start()