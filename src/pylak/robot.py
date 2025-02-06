
"""
Resumé:
En robot som man kan øve sig på basale programmerings principper

Direkte mål:
Lære om brug af funktioner, 

Indirekte mål:
Lære om automatisering og hvor programmering bruges i maskin industrien

Maintainer: VYD
"""

from .engine import Engine
import pyglet as pgl
import numpy as np
import math
from random import randint
from typing import Generator

    
DEFAULTVELOCITY = 50

class RobotArm:

    def __init__(self):
        self.batch = pgl.shapes.Batch()

        self.basepos = np.array([300, 100])
        
        
        self.link1 = pgl.shapes.Line(0, 0, 0, 0, batch=self.batch)
        self.link2 = pgl.shapes.Line(0, 0, 0, 0, batch=self.batch)
        

        # 2 joints (2 links)
        # Revolute Joints (rotary joints)

        self.L1 = 200
        self.L2 = 100
        self.velocity = 1/50

        # two joints
        self.joints = np.array([2*math.pi/3,math.pi/2])
        self._dest = np.array([0.0,0.0])

        # position
        self.pos = self.__FK__(*self.joints)

        # end point
        self.endPoint = pgl.shapes.Circle(*self.pos, 10, batch=self.batch)


    def __inverseJacobian__(self, theta1, theta2):
        
        # expensive should use -> Moore–Penrose pseudoinverse
        return np.linalg.inv(np.array([
            [-math.sin(theta1)*self.L1, -math.sin(theta2)*self.L2],
            [math.cos(theta1)*self.L1, -math.cos(theta2)*self.L2]
        ]))


    def __FK__(self, theta1, theta2):
        return self.basepos + np.array([
            math.cos(theta1)*self.L1 + math.cos(theta2)*self.L2,
            math.sin(theta1)*self.L1 + math.sin(theta2)*self.L2,
        ])


    def __IK__(self, pos):
        
        goal = np.array(pos)

        dx = np.array([1, 1])
        for i in range(300000):
            
            error = ( goal - self.__FK__(*dx) )

            dx = self.__inverseJacobian__(*dx) @ error + dx

            if np.linalg.norm(error) < 1:
                return dx

        return None


    def setDestination(self, pos):
        res = self.__IK__(pos)
        
        if res is None:
            raise ValueError('Position is not avaliable')

        self._dest = res


        self._dest = np.array([math.radians(round(i*(180/math.pi))%360) for i in self._dest])

        n = self._dest - self.joints

        norm = np.linalg.norm(n)

        self.steps = norm / self.velocity
        self._jointChange = self.velocity * (n / norm)



    def moveUp(self, v=DEFAULTVELOCITY):
        self.setDestination(self.pos + np.array([0, v]))


    def moveDown(self, v=DEFAULTVELOCITY):
        self.moveUp(-v)


    def moveLeft(self, v=DEFAULTVELOCITY):
        self.setDestination(self.pos + np.array([v, 0]))


    def moveRight(self, v=DEFAULTVELOCITY):
        self.moveLeft(-v)


    # update
    def update(self):

        if self.steps > 0:
            self.joints += self._jointChange
            self.steps -= 1
            
        else:
            self._onFinishCallback.__next__()

        self.x, self.y = self.__FK__(*self.joints)

        p1 = self.basepos + np.array([
            math.cos(self.joints[0])*self.L1,
            math.sin(self.joints[0])*self.L1
        ])

        self.link1.x, self.link1.y = self.basepos
        self.link1.x2, self.link1.y2 = p1
        self.link2.x, self.link2.y = p1
        self.link2.x2, self.link2.y2 = self.x, self.y


    def onFinish(self, callback):
        self._onFinishCallback = callback


    def draw(self):
        self.endPoint.x = self.x
        self.endPoint.y = self.y

        self.batch.draw()


    
# basic scene
class RobotSimulation:
    
    def __init__(self, program, *robots:list):
        self.robots:list[RobotArm] = robots
        
        self.program:Generator = program()

        for robot in self.robots:
            robot.onFinish(self.program)

        self.engine = Engine()

    
    def setup(self):
        
        self.program.__next__()

    
    def update(self):
        
        for robot in self.robots:
            robot.update()


    def draw(self):
        
        for robot in self.robots:
            robot.draw()


    def start(self):
        self.engine.setCurrentScene(self)
        self.engine.start()