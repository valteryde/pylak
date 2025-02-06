
"""

References

https://pyglet.readthedocs.io/en/latest/programming_guide/image.html#animations

For some reason binding animations to texture atlas creates problems

"""

import pyglet as pgl
from PIL import Image


class Animations:

    def __init__(self, texturePath:str, rows:int, cols:int, period=0.1):

        sprite_sheet = pgl.resource.image(texturePath)
        self.animations = []

        for _ in range(rows):
            
            image_grid = pgl.image.ImageGrid(sprite_sheet, rows=1, columns=cols)
            animation = image_grid.get_animation(period=period)
            self.animations.append( pgl.sprite.Sprite(img=animation) )

        self._currentAnimationIndex = 0


    def switch(self, index:int):
        self._currentAnimationIndex = index


    def draw(self):
        self.animations[self._currentAnimationIndex].draw()