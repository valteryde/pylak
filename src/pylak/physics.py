
from .collider import Collider
import numpy as np

###########################################
# PhysicsObject
###########################################
class PhysicsObject:
    """
    Physicsobjektets eneste mål er at ændre self.x og self.y på objektet

    Husk at dette objekt IKKE ændrer hvad der tegnes. Det skal man selv gøre

    """

    # 100 px svarer til 1 meter

    def __init__(self, object, collider:Collider, mass=100, immovable=False, drag=1):
        self.collider = collider # use objects collider
        self.collider._physicsObject = self # add reference to physics object in collider
        self.object = object
        self.immovable = immovable

        # add x and y to objects
        if not hasattr(object, 'x') or not hasattr(object, 'y'):
            print(object, 'har ingen x eller y. Dette tilføjes nu')
            object.x = collider.x
            object.y = collider.y

        self.collider._lastpos = [collider.x, collider.y]

        self.mass = mass

        self.velocity = np.array([0.0,0.0])
        self.forces = np.array([0.0,0.0])

        self.drag = drag * mass
        

    def addForce(self, x, y):
        self.forces += np.array([x, y])
    

    def update(self, engine, dt):

        # calculate drag
        if abs(self.velocity[0]) > 0:
            self.forces[0] -= self.drag * self.velocity[0]
        
        if abs(self.velocity[1]) > 0:
            self.forces[1] -= self.drag * self.velocity[1]
        
        # calculate velocity
        self.velocity += self.forces / self.mass * dt

        # reset forces
        self.forces = np.array([0.0, 0.0])

        # calculate inertia
        for collider in engine.collisions[self.collider]:
            
            if not hasattr(collider, '_physicsObject'):
                continue

            physics:PhysicsObject = collider._physicsObject

            velIndex, direction = self.__checkWhichSideCollision__(collider)

            if velIndex == None:
                continue

            # laver kun beregning for største objekt
            if physics.mass > self.mass:
                                
                va1 = self.velocity[velIndex]
                vb1 = physics.velocity[velIndex]

                va = ((self.mass - physics.mass) * va1 + (2 * physics.mass) * vb1) / (self.mass + physics.mass)
                vb = ((2 * self.mass) * va1 + (physics.mass - self.mass) * vb1) / (self.mass + physics.mass)

                self.velocity[velIndex] = va
                physics.velocity[velIndex] = vb

        # update position
        self.object.x += (self.velocity[0] * dt) * 1000
        self.object.y += (self.velocity[1] * dt) * 1000

        # force borders
        for collider in engine.collisions[self.collider]:
        
            # if physics.mass > self.mass:
                # fjern overlap
                if velIndex == 0:

                    if direction == 1:
                        self.object.x = min(self.object.x + self.collider.width, physics.collider.x) - self.collider.width
                    
                    if direction == -1:
                        self.object.x = max(self.object.x, physics.collider.x + physics.collider.width)

                else:
                        
                    if direction == 1:
                        self.object.y = min(self.object.y + self.collider.height, physics.collider.y) - self.collider.height
                    
                    if direction == -1:
                        self.object.y = max(self.object.y, physics.collider.y + physics.collider.height)

        # update last position
        if self.immovable:
            self.object.x = self.collider._lastpos[0]
            self.object.y = self.collider._lastpos[1]
            self.velocity = np.array([0.0,0.0])
        
        self.collider.x = self.object.x
        self.collider.y = self.object.y

        self.collider._lastpos = [self.object.x, self.object.y]


    def __checkWhichSideCollision__(self, other):
        """
        returns (velocity index, direction)
        """

        self.width = self.collider.width
        self.height = self.collider.height

        ox, oy = other._lastpos
        sx, sy = self.collider._lastpos

        dx = (sx + self.width / 2) - (ox + other.width / 2)
        dy = (sy + self.height / 2) - (oy + other.height / 2)
        width = (self.width + other.width) / 2
        height = (self.height + other.height) / 2
        crossWidth = width * dy
        crossHeight = height * dx

        if abs(dx) <= width and abs(dy) <= height:
            if crossWidth > crossHeight:
                if crossWidth > -crossHeight:
                    return (1, -1) #bottom
                else:
                    return (0, 1) #left
            else:
                if crossWidth > -crossHeight:
                    return (0, -1) # right
                else:
                    return (1, 1) # top
        return None, None
