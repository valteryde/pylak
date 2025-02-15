
"""

References

https://pyglet.readthedocs.io/en/latest/programming_guide/image.html#animations

For some reason binding animations to texture atlas creates problems

"""

import pyglet as pgl
from PIL import Image


class Animations:

    
    def __addAnimationState__(self, 
                              fullSpriteSheet, 
                              size, 
                              y0, 
                              y1, 
                              cols, 
                              period, 
                              rowHeight,
                              flipx=False,
                              flipy=False
                              ):

        # chop images into diffrent textures
        spriteSheet = fullSpriteSheet.crop([0, y0, fullSpriteSheet.width, y1])
        rawImage = spriteSheet.tobytes()  # tostring is deprecated
        spriteSheet = pgl.image.ImageData(spriteSheet.width, spriteSheet.height, 'RGBA', rawImage, pitch=-spriteSheet.width * 4)

        # load image into image grid and add animation
        imageGrid = pgl.image.ImageGrid(spriteSheet, rows=1, columns=cols)
        
        animation = imageGrid.get_animation(period=period)
        
        for frame in animation.frames:
            texture = frame.image.get_texture()
            frame.image = texture.get_transform(flipx, flipy)

        sprite = pgl.sprite.Sprite(img=animation)

        sprite.scale = size/rowHeight

        return sprite


    def __init__(self, texturePath:str, rows:int, cols:int, period=1/15, size=100):
        """
        uses center pos
        """

        self.size = size


        fullSpriteSheet = Image.open(texturePath)
        rowHeight = fullSpriteSheet.height / rows
        
        self.cols = cols
        self.rows = rows

        self.animations = {
            "default":[],
            "flipx":[],
            "flipy":[]
        }

        self._forceNext = None
        self._forceNextActive = False

        for i in range(rows):

            self.animations["default"].append(self.__addAnimationState__(
                fullSpriteSheet, 
                size,
                rowHeight*i, 
                rowHeight*(i+1), 
                cols, 
                period, 
                rowHeight
            ))

        for i in range(rows):

            self.animations["flipx"].append(self.__addAnimationState__(
                fullSpriteSheet, 
                size,
                rowHeight*i, 
                rowHeight*(i+1), 
                cols, 
                period, 
                rowHeight,
                flipx=True
            ))
        
        for i in range(rows):

            self.animations["flipy"].append(self.__addAnimationState__(
                fullSpriteSheet, 
                size,
                rowHeight*i, 
                rowHeight*(i+1), 
                cols, 
                period, 
                rowHeight,
                flipy=True
            ))

        self._currentAnimation = [0, 'default']
        self._nextAnimationIndex = 0
        self._reachedEndOfCycle = False
        
        self.x = 0 # center pos
        self.y = 0


    def switch(self, index:int, flipx:bool=False, flipy:bool=False):
        """
        Bruges til states
        """
        
        if flipx and flipy:
            raise NotImplemented('Both flips can not happened at once')

        state = 'default'
        if flipx: state = 'flipx'
        if flipy: state = 'flipy'

        self._nextAnimationIndex = index
        self._currentAnimation[1] = state


    def do(self, index:int, flipx:bool=False, flipy:bool=False):
        
        self.switch(index, flipx, flipy)

        self._forceNext = self._nextAnimationIndex


    def setPos(self, x, y):
        self.x = x
        self.y = y


    def draw(self, x=None, y=None):

        if x is not None:
            self.x = x
        
        if y is not None:
            self.y = y


        index, state = self._currentAnimation

        sprite:pgl.sprite.Sprite = self.animations[state][index]
        sprite.x = x + (state == "flipx") * self.size - self.size/2
        sprite.y = y + (state == "flipy") * self.size - self.size/2

        # denne burde kun køre en gang per cyklus men bliver kørt flere gange 
        # hver gang der tegnes og man er på det sidste frame
        if sprite.frame_index == self.cols - 1 and not self._reachedEndOfCycle:
            
            # hvis der er en ny forced animation som ikke er igang
            if self._forceNext and not self._forceNextActive:
                # så skal den sættes på nu, da animations cyklussen er klar 
                self._forceNextActive = True
                self._currentAnimation[0] = self._forceNext
            
            # hvis den forced animation er der og har været igang
            elif self._forceNext and self._forceNextActive:
                # så skal den sættes fjerens nu da animationen er done
                self._forceNext = None
                self._forceNextActive = False
                self._currentAnimation[0] = self._nextAnimationIndex

            # hvis der ingen forced er
            else:
                self._currentAnimation[0] = self._nextAnimationIndex
            
        self._reachedEndOfCycle = sprite.frame_index == self.cols - 1

        sprite.draw()