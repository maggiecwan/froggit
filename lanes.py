"""
Lanes module for Froggit

This module contains the lane classes for the Frogger game. The lanes are the vertical
slice that the frog goes through: grass, roads, water, and the exit hedge.

Each lane is like its own level. It has hazards (e.g. cars) that the frog has to make
it past.  Therefore, it is a lot easier to program frogger by breaking each level into
a bunch of lane objects (and this is exactly how the level files are organized).

You should think of each lane as a secondary subcontroller.  The level is a subcontroller
to app, but then that subcontroller is broken up into several other subcontrollers, one
for each lane.  That means that lanes need to have a traditional subcontroller set-up.
They need their own initializer, update, and draw methods.

There are potentially a lot of classes here -- one for each type of lane.  But this is
another place where using subclasses is going to help us A LOT.  Most of your code will
go into the Lane class.  All of the other classes will inherit from this class, and
you will only need to add a few additional methods.

If you are working on extra credit, you might want to add additional lanes (a beach lane?
a snow lane?). Any of those classes should go in this file.  However, if you need additional
obstacles for an existing lane, those go in models.py instead.  If you are going to write
extra classes and are now sure where they would go, ask on Piazza and we will answer.

# Maggie Wan (mw695)
# 12/21/2020
"""
from game2d import *
from consts import *
from models import *

# PRIMARY RULE: Lanes are not allowed to access anything in any level.py or app.py.
# They can only access models.py and const.py. If you need extra information from the
# level object (or the app), then it should be a parameter in your method.

class Lane(object):         # You are permitted to change the parent class if you wish
    """
    Parent class for an arbitrary lane.

    Lanes include grass, road, water, and the exit hedge.  We could write a class for
    each one of these four (and we will have classes for THREE of them).  But when you
    write the classes, you will discover a lot of repeated code.  That is the point of
    a subclass.  So this class will contain all of the code that lanes have in common,
    while the other classes will contain specialized code.

    Lanes should use the GTile class and to draw their background.  Each lane should be
    GRID_SIZE high and the length of the window wide.  You COULD make this class a
    subclass of GTile if you want.  This will make collisions easier.  However, it can
    make drawing really confusing because the Lane not only includes the tile but also
    all of the objects in the lane (cars, logs, etc.)
    """

    # LIST ALL HIDDEN ATTRIBUTES HERE

    #Attribute _source: the image source of the GTile for the lane
    #Invariant: _source must be a string

    #Attribute _height: the height of the lane
    #Invariant: _height must be > 0

    #Attribute _width: the width of the lane
    #Invariant: _width must be an int and > 0

    #Attribute _objs: the list of objects in the lane
    #Invariant: _objs must be a list

    #Attribute _speed: the speed at which the objects are moving
    #Invariant: _speed must be an int and > 0

    #Attribute _offscreen: the offscreen value
    #Invariant: _offscreen must be an int and > 0

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getX(self):
        """
        Returns x-value of lane.
        """
        return self.x

    def setX(self,value):
        """
        Sets x-value of lane to value.
        """
        self.x = value

    def getY(self):
        """
        Returns y-value of lane.
        """
        return self.y

    def setY(self,value):
        """
        Sets y-value of lane to value.
        """
        self.y = value

    def getTile(self):
        """
        Returns tile attribute.
        """
        return self._tile

    def getObjects(self):
        """
        Returns list of objects in lane.
        """
        return self._objs

    def getSpeed(self):
        """
        Returns speed of objects.
        """
        return self._speed

    # INITIALIZER TO SET LANE POSITION, BACKGROUND,AND OBJECTS
    def __init__(self,level,pos,dict,offscreen,hitboxDict):

        self._source = str(dict['type'])+'.png'
        self._height = GRID_SIZE
        self._width = level.getWidth() * GRID_SIZE
        self._objs = []
        self._speed = 0
        self._offscreen = offscreen
        self.x = 0
        self.y = self._height*pos


        if 'speed' in dict:
            self._speed = dict['speed']


        self._tile = GTile(source = self._source,height=self._height,
                     width=self._width,left=0,bottom=self._height*pos)


        if 'objects' in dict:
            for key in dict['objects']:
                ht = hitboxDict[key['type']]['hitbox']
                image = GImage(source = key['type'] + '.png',
                        x = key['position']*GRID_SIZE+GRID_SIZE//2,y=self._tile.y)

                image.hitbox = ht

                if self._speed < 0:
                    image.angle = 180
                self._objs.append(image)

    def update(self,input,dt):
        """
        Updates the game objects each frame.

        For all of the objects in the individual lanes (cars,logs,etc),
        it moves them and wraps them around to reappear on the screen.

        Parameter input: user input
        Precondition: inut is a GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """

        for object in self._objs:

            if self._speed < 0:
                object.x = object.x + (self._speed * dt)
                if object.x < -self._offscreen*GRID_SIZE:
                    d =(-self._offscreen*GRID_SIZE) - object.x
                    object.x = self._width + self._offscreen*GRID_SIZE - d


            if self._speed > 0:
                    object.x = object.x + (self._speed * dt)
                    if object.x > self._width + self._offscreen*GRID_SIZE:
                        d = object.x - (self._width + self._offscreen*GRID_SIZE)
                        object.x = -self._offscreen*GRID_SIZE + d
    # ADDITIONAL METHODS (DRAWING, COLLISIONS, MOVEMENT, ETC)
    def draw(self,view):
        """
        Draws the game objects to the view.

        It draws each tile for the lanes in the level and the GImages of
        the objects in each lane.

        Parameter view:
        Precondition:
        """
        self._tile.draw(view)

        for objects in self._objs:
            objects.draw(view)


class Grass(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a 'safe' grass area.

    You will NOT need to actually do anything in this class.  You will only do anything
    with this class if you are adding additional features like a snake in the grass
    (which the original Frogger does on higher difficulties).
    """
    def __init__(self,level,pos,dict,offscreen,htImageDict):
        super().__init__(level=level,pos=pos,dict=dict,offscreen=offscreen,
                         hitboxDict=htImageDict)
        self._tile.source = 'grass.png'
    # ONLY ADD CODE IF YOU ARE WORKING ON EXTRA CREDIT EXTENSIONS.


class Road(Lane):                           # We recommend AGAINST changing this one
    """
    A class representing a roadway with cars.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, roads are different
    than other lanes as they have cars that can kill the frog. Therefore, this class
    does need a method to tell whether or not the frog is safe.
    """
    # GETTERS AND SETTERS
    def carPos(self): #Getter for car pos
        """
        Loops through objects in lane and returns list of cars.
        """
        cars = []
        if self._objs != []:
            for object in self._objs:
                cars.append(object)
        return cars

    def __init__(self,level,pos,dict,offscreen,htImageDict):
        super().__init__(level=level,pos=pos,dict=dict,offscreen=offscreen,
                         hitboxDict=htImageDict)
        self._tile.source = 'road.png'
        # DEFINE ANY NEW METHODS HERE


class Water(Lane):
    """
    A class representing a waterway with logs.

    If you implement Lane correctly, you do really need many methods here (not even an
    initializer) as this class will inherit everything.  However, water is very different
    because it is quite hazardous. The frog will die in water unless the (x,y) position
    of the frog (its center) is contained inside of a log. Therefore, this class needs a
    method to tell whether or not the frog is safe.

    In addition, the logs move the frog. If the frog is currently in this lane, then the
    frog moves at the same rate as all of the logs.
    """
    def getLogs(self):
        """
        Loops through list of objects in lane and returns list of logs.
        """
        logs = []
        if self._objs != []:
            for object in self._objs:
                if 'log' in  object.source :
                    logs.append(object)
        return logs

    def __init__(self,level,pos,dict,offscreen,htImageDict):
        super().__init__(level=level,pos=pos,dict=dict,offscreen=offscreen,
                        hitboxDict=htImageDict)
        self._tile.source = 'water.png'
        # DEFINE ANY NEW METHODS HERE


class Hedge(Lane):
    """
    A class representing the exit hedge.

    This class is a subclass of lane because it does want to use a lot of the features
    of that class. But there is a lot more going on with this class, and so it needs
    several more methods.  First of all, hedges are the win condition. They contain exit
    objects (which the frog is trying to reach). When a frog reaches the exit, it needs
    to be replaced by the blue frog image and that exit is now "taken", never to be used
    again.

    That means this class needs methods to determine whether or not an exit is taken.
    It also need to take the (x,y) position of the frog and use that to determine which
    exit (if any) the frog has reached. Finally, it needs a method to determine if there
    are any available exits at all; once they are taken the game is over.

    These exit methods will require several additional attributes. That means this class
    (unlike Road and Water) will need an initializer. Remember to user super() to combine
    it with the initializer for the Lane.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getExits(self):
        """
        Loops through list of objects and returns list of exits.
        """
        exits = []
        if self._objs != []:

            for object in self._objs:
                if object.source == 'exit.png':
                    exits.append(object)
        return exits

    def getOpenings(self):
        """
        Loops through list of objects and returns list of openings.
        """
        openings = []
        if self._objs != []:
            for object in self._objs:
                if object.source == 'open.png':
                    openings.append(object)
        return openings

            # INITIALIZER TO SET ADDITIONAL EXIT INFORMATION
    def __init__(self,level,pos,dict,offscreen,htImageDict):
        super().__init__(level=level,pos=pos,dict=dict,offscreen=offscreen,
                         hitboxDict=htImageDict)
        self._tile.source = 'hedge.png'

        self._exitsOccupied = []
        self._allExitsOccupied = True
        if self._objs != []:
            for object in self._objs:
                if object.source == 'exit.png':
                    self._exitsOccupied.append(0)




    # ANY ADDITIONAL METHODS


# IF YOU NEED ADDITIONAL LANE CLASSES, THEY GO HERE
