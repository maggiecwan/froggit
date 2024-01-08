"""
Models module for Froggit

This module contains the model classes for the Frogger game. Anything that you
interact with on the screen is model: the frog, the cars, the logs, and so on.

Just because something is a model does not mean there has to be a special class for
it. Unless you need something special for your extra gameplay features, cars and logs
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object.

That is why this module contains the Frog class.  There is A LOT going on with the
frog, particularly once you start creating the animation coroutines.

If you are just working on the main assignment, you should not need any other classes
in this module. However, you might find yourself adding extra classes to add new
features.  For example, turtles that can submerge underneath the frog would probably
need a custom model for the same reason that the frog does.

If you are unsure about  whether to make a new class or not, please ask on Piazza. We
will answer.

# Maggie Wan (mw695)
# 12/21/2020
"""
from consts import *
from game2d import *
import introcs
import random
import math
import time
import random
# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from a lane or level object, then it
# should be a parameter in your method.
ANIMATION_SPEED = 1

class Frog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAngle(self):
        """
        Returns angle of frog.
        """
        return self.angle

    def setAngle(self,value):
        """
        Sets angle of frog to value.
        """
        assert type(value) == int or type(value) == float
        self.angle = value

    def getX(self):
        """
        Returns x-value of frog.
        """
        return self.x

    def setX(self,value):
        """
        Sets x-value of frog to value.
        """
        assert type(value)==int or type(value)==float
        self.x = value

    def getY(self):
        """
        Returns y-value of frog.
        """
        return self.y

    def setY(self,value):
        """
        Sets y-value of frog to value.
        """
        assert type(value)==int or type(value)==float
        assert value >=0
        self.y = value

    # INITIALIZER TO SET FROG POSITION
    def __init__(self,x,y,sFrog):
        super().__init__(x=x,y=y,width=sFrog['size'][0],height=sFrog['size'][1],
                source=sFrog['file'],format=(sFrog['format'][0],sFrog['format'][1]))
        self.angle = FROG_NORTH
        self.animator = None
        self.hitboxes = sFrog['hitboxes']
        self.direction = 0 # Doing this prevents a slow down due to initialization
        self.frame = 0
        self.visible = True

    def animate_slideV(self,direction,maxHeight):
        """
        Animates a  vertical up or down of the image over ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up' or 'down'.

        Parameter maxHeight: maximum amount of vertical distance to travel
        Precondition: maxHeight must be greater than 0
        """
        svert = self.getY()
        if direction == 'up':
            fvert = svert+GRID_SIZE
        else:
            fvert = svert-GRID_SIZE
        steps = GRID_SIZE/FROG_SPEED
        animating = True
        frameNum = 0
        while animating:
            dt = (yield)
            amount = steps*dt
            if direction == 'up':
                self.setY(self.getY()+amount)
            else:
                self.setY(self.getY()-amount)

            if self.getAngle() == FROG_SOUTH and self.getY()-GRID_SIZE <= 0 :
                self.setY(GRID_SIZE/2)
                animating = False
            elif self.getAngle() == FROG_NORTH and maxHeight-self.getY()-GRID_SIZE <= 0 :
                self.setY(maxHeight-self._height)
                animating = False
            elif abs(self.getY()-svert) >= GRID_SIZE:
                self.setY(fvert)
                animating = False

            self._setFrameUp(svert)
            self._setFrameDown(svert)

    def animate_slideH(self,direction, maxWidth):
        """
        Animates a  vertical up or down of the image over ANIMATION_SPEED seconds

        This method is a coroutine that takes a break (so that the game
        can redraw the image) every time it moves it. The coroutine takes
        the dt as periodic input so it knows how many (parts of) seconds
        to animate.

        Parameter dt: The time since the last animation frame.
        Precondition: dt is a float.

        Parameter direction: The direction to slide.
        Precondition: direction is a string and one of 'up' or 'down'.

        Parameter maxHeight: maximum amount of horizontal distance to travel
        Precondition: maxHeight must be greater than 0
        """
        svert = self.getX()
        if direction == 'right':
            fvert = svert+GRID_SIZE
        else:
            fvert = svert-GRID_SIZE
        steps = GRID_SIZE/FROG_SPEED
        animating = True
        frameNum = 0

        while animating:
            dt = (yield)
            amount = steps*dt
            if direction =='left':
                self.setX(self.getX()-amount)
            else:
                self.setX(self.getX()+amount)
            if self.getAngle() == FROG_WEST and self.getX()-GRID_SIZE <= 0:
                self.frame = 0
                self.setX(self._width)
                animating = False
            if self.getAngle() == FROG_EAST and maxWidth -self.getX()-GRID_SIZE <= 0:
                self.frame = 0
                self.setX(maxWidth - self._width)
                animating = False
            if abs(self.getX()-svert) >= GRID_SIZE:
                self.setX(fvert)
                animating = False
            self._setFrameLeft(svert)
            self._setFrameRight(svert)

    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def _setFrameUp(self,svert):
        """
        Sets the frames for the frog animation.

        Divides the distance that the frog travels and assigns the frames
        from 0 to 4 and then back down to display the frog as stretching
        out and then contracting.

        Parameter svert: distance the frog travels
        Precondition: svert is an int or float
        """

        distance = self.getY()-svert
        if distance > 8 and distance < 16:
            self.frame = 1
        if distance > 16 and distance < 24:
            self.frame = 2
        if distance > 24 and distance < 32:
            self.frame = 3
        if distance > 32 and distance < 40:
            self.frame = 4
        if distance > 40 and distance < 48:
            self.frame = 3
        if distance > 48 and distance < 56:
            self.frame = 2
        if distance >  56 and distance < 64:
            self.frame = 1
        if round(distance) >= 64:
            self.frame = 0

    def _setFrameDown(self,svert):
        """
        Sets the frames for the frog animation.

        Divides the distance that the frog travels and assigns the frames
        from 0 to 4 and then back down to display the frog as stretching
        out and then contracting.

        Parameter svert: distance the frog travels
        Precondition: svert is an int or float
        """
        distance = svert - self.getY()
        if distance > 8 and distance < 16:
            self.frame = 1
        if distance > 16 and distance < 24:
            self.frame = 2
        if distance > 24 and distance < 32:
            self.frame = 3
        if distance > 32 and distance < 40:
            self.frame = 4
        if distance > 40 and distance < 48:
            self.frame = 3
        if distance > 48 and distance < 56:
            self.frame = 2
        if distance >  56 and distance < 64:
            self.frame = 1
        if round(distance) >= 64:
            self.frame = 0

    def _setFrameRight(self,svert):
        """
        Sets the frames for the frog animation.

        Divides the distance that the frog travels and assigns the frames
        from 0 to 4 and then back down to display the frog as stretching
        out and then contracting.

        Parameter svert: distance the frog travels
        Precondition: svert is an int or float
        """
        distance = self.getX()-svert
        if distance > 8 and distance < 16:
            self.frame = 1
        if distance > 16 and distance < 24:
            self.frame = 2
        if distance > 24 and distance < 32:
            self.frame = 3
        if distance > 32 and distance < 40:
            self.frame = 4
        if distance > 40 and distance < 48:
            self.frame = 3
            if distance == 46.0:
                self.frame = 0
        if distance > 48 and distance < 56:
            self.frame = 2
        if distance >  56 and distance < 64:
            self.frame = 1
        if round(distance) >= 64:
            self.frame = 0

    def _setFrameLeft(self,svert):
        """
        Sets the frames for the frog animation.

        Divides the distance that the frog travels and assigns the frames
        from 0 to 4 and then back down to display the frog as stretching
        out and then contracting.

        Parameter svert: distance the frog travels
        Precondition: svert is an int or float
        """
        distance = svert - self.getX()
        if distance > 8 and distance < 16:
            self.frame = 1
        if distance > 16 and distance < 24:
            self.frame = 2
        if distance > 24 and distance < 32:
            self.frame = 3
        if distance > 32 and distance < 40:
            self.frame = 4
        if distance > 40 and distance < 48:
            self.frame = 3
            if distance == 46.0:
                self.frame = 0
        if distance > 48 and distance < 56:
            self.frame = 2
        if distance >  56 and distance < 64:
            self.frame = 1
        if round(distance) >= 64:
            self.frame = 0


class DeadFrog(GSprite):         # You will need to change this by Task 3
    """
    A class representing the frog

    The frog is represented as an image (or sprite if you are doing timed animation).
    However, unlike the obstacles, we cannot use a simple GImage class for the frog.
    The frog has to have additional attributes (which you will add).  That is why we
    make it a subclass of GImage.

    When you reach Task 3, you will discover that Frog needs to be a composite object,
    tracking both the frog animation and the death animation.  That will like caused
    major modifications to this class.
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getAngle(self):
        """
        Returns angle of dead frog.
        """
        return self.angle

    def setAngle(self,value):
        """
        Sets dead frog angle to value.
        """
        assert type(value) == int or type(value) == float
        self.angle = value

    def getX(self):
        """
        Returns x-value of dead frog.
        """
        return self.x

    def setX(self,value):
        """
        Sets x-value of dead frog to value.
        """
        assert type(value)==int or type(value)==float
        self.x = value

    def getY(self):
        """
        Returns y-value of dead frog.
        """
        return self.y

    def setY(self,value):
        """
        Sets y-value of dead frog to value.
        """
        assert type(value)==int or type(value)==float
        assert value >=0
        self.y = value

    # INITIALIZER TO SET FROG POSITION
    def __init__(self,x,y,sFrog):
        super().__init__(x=x,y=y,width=sFrog['size'][0],height=sFrog['size'][1],
                source=sFrog['file'],format=(sFrog['format'][0],sFrog['format'][1]))
        self.angle = FROG_NORTH
        self.animator = None
        self.direction = 0 # Doing this prevents a slow down due to initialization
        self.frame = 0
        self.visible = False

    def animate(self):
        """
        Animates the death sprite.

        Based on number of frames and duration of the death graphics,
        it runs the coroutine to display the death of the frog.
        """
        animating = True
        duration = 0
        frameNum = 0

        while animating:
            dt = (yield)
            duration += dt

            self.frame = frameNum
            if duration >= 0 and duration < 0.0625:
                frameNum = 1
            if duration >= 0.0625 and duration < 0.125:
                frameNum = 2
            if duration >= 0.125 and duration < 0.1875:
                frameNum = 3
            if duration >= 0.1875 and duration < 0.25:
                frameNum = 4
            if duration >= 0.25 and duration < 0.3175:
                frameNum = 5
            if duration >= 0.3175 and duration < 0.38:
                frameNum = 6
            if duration >= 0.38 and duration < 0.4425:
                frameNum = 7
            if duration >= DEATH_SPEED:
                frameNum = 0
                self.visible = False
                self.animator = None
                animating = False
