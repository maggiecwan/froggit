"""
Subcontroller module for Froggit

This module contains the subcontroller to manage a single level in the Froggit game.
Instances of Level represent a single game, read from a JSON.  Whenever you load a new
level, you are expected to make a new instance of this class.

The subcontroller Level manages the frog and all of the obstacles. However, those are
all defined in models.py.  The only thing in this class is the level class and all of
the individual lanes.

This module should not contain any more classes than Levels. If you need a new class,
it should either go in the lanes.py module or the models.py module.

# Maggie Wan (mw695)
# 12/21/2020
"""
from game2d import *
from consts import *
from lanes  import *
from models import *

# PRIMARY RULE: Level can only access attributes in models.py or lanes.py using getters
# and setters. Level is NOT allowed to access anything in app.py (Subcontrollers are not
# permitted to access anything in their parent. To see why, take CS 3152)


class Level(object):
    """
    This class controls a single level of Froggit.

    This subcontroller has a reference to the frog and the individual lanes.  However,
    it does not directly store any information about the contents of a lane (e.g. the
    cars, logs, or other items in each lane). That information is stored inside of the
    individual lane objects.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lesson 27 for an example.  This class will be similar to that
    one in many ways.

    All attributes of this class are to be hidden.  No attribute should be accessed
    without going through a getter/setter first.  However, just because you have an
    attribute does not mean that you have to have a getter for it.  For example, the
    Froggit app probably never needs to access the attribute for the Frog object, so
    there is no need for a getter.

    The one thing you DO need a getter for is the width and height.  The width and height
    of a level is different than the default width and height and the window needs to
    resize to match.  That resizing is done in the Froggit app, and so it needs to access
    these values in the level.  The height value should include one extra grid square
    to suppose the number of lives meter.
    """
    # LIST ALL HIDDEN ATTRIBUTES HERE

    #Attribute _height: the current height of the game
    #Invariant: _height must be an int and > 0

    #Attribute _version: the current level version of the game
    #Invariant: _version must be a float

    #Attribute _x: the current x-value
    #Invariant: _x must be an int and > 0

    #Attribute _y: the current y-value
    #Invariant: _y must be an int and > 0

    #Attribute _offscreen: value to support movement wrap
    #Invariant: _offscreen must be an int

    #Attribute _lanes: list of lanes
    #Invariant: _lanes must be a list

    #Attribute _noOfLives: value representing the initial number of lives
    #Invariant: _noOfLives must be an int

    #Attribute _lives: list containing images for lives to be displayed
    #Invariant: _lives must be list

    #Attribute _cooldown: time before frog can move again
    #Invariant: _cooldown must be > 0

    #Attribute _safeFrogs: list containing safe frog images to be displayed
    #Invariant: _safeFrogs: must be a list

    #Attribute _allOccupied: True if the exits are occupied, False otherwise
    #Invariant: _allOccupied: must be a bool

    #Attribute _onlog: True if frog is on log, None otherwise
    #Invariant: _onlog: must be None or True

    #Attribute _exit: list containing safe frog images to be displayed
    #Invariant: _exit: must be a list

    #Attribute _htImageDict: hitbox value of image
    #Invariant: _htImageDict: must be an int

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getWidth(self):
        """
        Returns width of level screen.
        """
        return self._width

    def setWidth(self,value):
        """
        Sets width of level to value.
        """
        assert type(value) == int or type(value) == float
        assert value > 0
        self._width = value

    def getHeight(self):
        """
        Returns height of level screen.
        """
        return self._height

    def setHeight(self,value):
        """
        Sets height of level to value.
        """
        assert type(value) == int or type(value) == float
        assert value > 0
        self._height = value

    def getPaused(self):
        """
        Returns paused attribute.
        """
        return self._paused

    def getFrog(self):
        """
        Returns frog attribute.
        """
        return self._frog

    def setFrog(self,value):
        """
        Sets frog attribute to value.
        """
        self._frog = value

    def getOccupied(self):
        """"
        Returns _allOccupied attribute.
        """
        return self._allOccupied

    def getX(self):
        """
        Returns x-value of level.
        """
        return self._x

    def getY(self):
        """
        Returns y-value of level.
        """
        return self._y

    def getLives(self):
        """
        Returns number of lives.
        """
        return self._noOfLives

    def getDeadFrog(self):
        """
        Returns dead frog attribute.
        """
        return self._deadfrog

    # INITIALIZER (standard form) TO CREATE THE FROG AND LANES
    def __init__(self,dict,htDict):

        self._version = dict['version']
        self._offscreen = dict['offscreen']
        self._width = dict['size'][0]
        self._height = dict['size'][1]
        self._x = dict['start'][0]
        self._y = dict['start'][1]
        self._lanes = []
        self._noOfLives = 3
        self._lives=[]
        self._cooldown = FROG_SPEED
        self._safeFrogs = []
        self._allOccupied = False
        self._onlog = None
        self._exit = None
        self._exitX = 0
        self._exitY = 0
        self._openingX = 0
        self._htImageDict = htDict['images']
        self.splatSound = Sound(SPLAT_SOUND)
        self.jumpSound = Sound(CROAK_SOUND)
        self.trillSound = Sound(TRILL_SOUND)

        pos = -1

        for lane in dict['lanes']:
            pos = pos+1
            if lane['type'] == 'grass':
                self._lanes.append(Grass(self,pos,lane,self._offscreen,
                                   self._htImageDict))

            if lane['type']== 'road':
                self._lanes.append(Road(self,pos,lane,self._offscreen,
                                   self._htImageDict))

            if lane['type'] == 'hedge':
                self._lanes.append(Hedge(self,pos,lane,self._offscreen,
                                   self._htImageDict))

            if lane['type'] == 'water':
                self._lanes.append(Water(self,pos,lane,self._offscreen,
                                   self._htImageDict))

        self._frog = Frog(x=self._x*GRID_SIZE+GRID_SIZE//2,
                     y=self._y*GRID_SIZE+GRID_SIZE//2,
                     sFrog=htDict['sprites']['frog'])
        self._deadfrog = DeadFrog(x=self._x*GRID_SIZE+GRID_SIZE//2,
                         y=self._y*GRID_SIZE+GRID_SIZE//2,
                         sFrog=htDict['sprites']['skulls'])
        self._frog.angle= FROG_NORTH
        self._bar = GLabel(text = "LIVES:",font_name = ALLOY_FONT,
                    font_size = ALLOY_SMALL, linecolor='dark green',
                    x=(self.getWidth()-self._noOfLives-1)*GRID_SIZE-ALLOY_SMALL/2,
                    y=(self.getHeight()+1)*GRID_SIZE -GRID_SIZE/2 )

        for i in range(self._noOfLives):
             life = GImage(source = FROG_HEAD,width=GRID_SIZE,height=GRID_SIZE,
                    y=(self.getHeight()+1)*GRID_SIZE - GRID_SIZE/2,
                    x=(self.getWidth()-i)*GRID_SIZE-GRID_SIZE/2)

             self._lives.append(life)

    def update(self,input,dt):
        """
        Updates the game objects each frame.

        It is in charge of playing the game. It calls _lane to draw
        the GTiles in each level and loops through the different arrow
        keys as input to move the frog, calling the animator.


        Parameter input: user input
        Precondition: input is a GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        for lane in self._lanes:
            lane.update(input,dt)
        dx = self._frog.getX()
        dy = self._frog.getY()
        if self._deadfrog != None and not self._deadfrog.animator is None:
            self.splatSound.play()
            try:
                self._deadfrog.animator.send(dt)
            except:
                self._deadfrog.animator = None
                self._frog = None
                self._updateLives()
        if self._frog != None and not self._frog.animator is None:
            self.jumpSound.play()
            try:
                self._frog.animator.send(dt)
            except:
                self._frog.animator = None
        elif input.is_key_down('left') and input.key_count == 1:
            self._keyLeft()
        elif input.is_key_down('right') and input.key_count == 1:
            self._keyRight()
        elif input.is_key_down('up') and input.key_count == 1:
            self._keyUp()
        elif input.is_key_down('down') and input.key_count == 1:
            self._keyDown()
        if self._containsLog(self._lanes,dt) != True:
            self._onlog = False
        if (self._frog != None and self._carCrash(self._lanes) == True
        or self._drown(self._lanes) == True or self._frogOut() == True):
            self._deadAnimate()

    def draw(self,view):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject. It calls
        lane to draw the GTiles for each lane and it also displys the
        GLabel for the Lives Bar as well as the GImages of the frog heads.
        When a frog succesfully reaches the exit, it draws the blue safe
        frog image.

        Parameter view: view to draw to
        Precondition: view is a GView
        """
        for lane in self._lanes:
            lane.draw(view)

        self._bar.draw(view)
        for life in  self._lives:
            life.draw(view)
        if not self._frog == None and self._frog.visible == True:
            self._frog.draw(view)

        if self._deadfrog != None and self._deadfrog.visible == True:
            self._deadfrog.draw(view)

        for frog in  self._safeFrogs:
            frog.draw(view)

    def _checkOccupied(self,lanes):
        """
        Checks if the exits in the level have been occupied.

        Loops through the exits in the hedge lane and if the frog
        has occupied all of them, it returns True.

        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list
        """
        allOccupied = True
        for lane in lanes:
            if lane.getTile().source == 'hedge.png':
                for i in range(len(lane.getExits())):
                    exit = lane.getExits()[i]
                    if  lane._exitsOccupied[i] == 0:
                        allOccupied = False
        return allOccupied

    def _collision(self,lanes):
        """
        Checks if the frog has collided with a hedge.

        Loops through the tiles in the hedge lane and if the frog
        collided with them, it returns True.

        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list
        """
        for lane in lanes:
            if lane.getTile().source == 'hedge.png' :
                if self._frog != None and self._frog.collides(lane.getTile()):
                    self._frog.setY(lane.getTile().y-GRID_SIZE)
                    return True

    def _containsLog(self,lanes,dt):
        """
        Checks if frog is on a log, and moves it along with the log if so.

        It also returns True if frog has jumped on log and turns the animator
        coroutine off, to allow the frog to ride on the log.

        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        for lane in lanes:
            if lane.getTile().source == 'water.png':
                for i in range(len(lane.getLogs())):
                    log = lane.getLogs()[i]
                    if (self._frog != None and log.contains((self._frog.getX(),
                       self._frog.getY()))):
                        self._onlog = True
                        speed = lane.getSpeed()
                        if speed < 0:
                            self._frog.setX(self._frog.x + (speed * dt))

                        if speed > 0:
                            self._frog.setX(self._frog.x + (speed * dt))

                        return True
        return False

    def _drown(self,lanes):
        """
        Checks if the frog has drowned in the water.

        It loops through the water lane and if frog has collided with it,
        it returns True if the frog has entered the water lane and is not on a
        log.

        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list
        """
        for lane in lanes:
            if lane.getTile().source == 'water.png':
                if self._frog != None and self._frog.collides(lane.getTile()):
                    if self._onlog != True and  self._frog.animator == None:
                        return True

    def _containsExit(self,lanes):
        """
        Checks if the frog is in an exit.

        Once the frog is contained in an exit, it returns True and changes the
        _allOccupied to True once all of the exits in the level have been
        occupied.

        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list
        """
        allOccupied = True
        for lane in lanes:
            if lane.getTile().source == 'hedge.png':
                for i in range(len(lane.getExits())):
                    exit = lane.getExits()[i]
                    self._exitX = exit.x
                    self._exitY = exit.y
                    if lane._exitsOccupied[i] == 0:
                        allOccupied = False
                        if exit.contains((self._frog.getX(),self._frog.getY()+GRID_SIZE)):
                            lane._exitsOccupied[i]=1
                            return True
        if allOccupied  == True :
            self._allOccupied = True
        return False

    def _containsOpening(self,lanes):
        """
        Checks if the frog is going through an opening.

        Loops through the hedge lane to look for the openings, and if the frog
        is contained within the tile, it returns True.

        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list
        """
        for lane in lanes:
            if lane.getTile().source == 'hedge.png':
                for i in range (len(lane.getOpenings())):
                    opening = lane.getOpenings()[i]
                    if opening.contains((self._frog.getX(),self._frog.getY()+GRID_SIZE)):
                        self._openingX = self._frog.getX()
                        return True
                return False

    def _updateLives(self):
        """
        Updates the lives bar on the upper right corner of the game.

        When a life is lost, the display subtracts one GObject from the list
        of frog heads.
        """
        if self._noOfLives >= 1:
            self._noOfLives = self._noOfLives-1
            self._bar = GLabel(text = "LIVES:",font_name = ALLOY_FONT,
                font_size = ALLOY_SMALL, linecolor='dark green',
                x=(self.getWidth()-self._noOfLives-1)*GRID_SIZE-ALLOY_SMALL/2,
                y=(self.getHeight()+1)*GRID_SIZE -GRID_SIZE/2 )
            self._lives = []
            for i in range(self._noOfLives):
                life = GImage(source = FROG_HEAD,width=GRID_SIZE,height=GRID_SIZE,
                y=(self.getHeight()+1)*GRID_SIZE - GRID_SIZE/2,
                x=(self.getWidth()-i)*GRID_SIZE-GRID_SIZE/2)
                self._lives.append(life)
        else:
            self._noOfLives = 0

    def _carCrash(self,lanes):
        """
        Checks if the frog has collided into a car.

        Loops through the road lanes and checks the position of the moving
        car objects and if the frog collides with it, it returns True.
        Parameter lanes: list of lanes in the level to loop through
        Precondition: lanes is a list
        """
        for lane in lanes:
            if lane.getTile().source == 'road.png':
                for i in range(len(lane.carPos())):
                    carpos = lane.carPos()[i]
                    if self._frog != None and self._frog.collides(carpos):
                        return True

    def _reachExit(self):
        """
        Checks if the frog has successfully reached the exit.

        Sets the frog to None and displays the blue safe frog image on the
        exit which the frog has entered.
        """

        self._frog = None
        self._safeFrogs.append(GImage(source=FROG_SAFE,x=self._exitX,
                         y=self._exitY))
        self.trillSound.play()

    def _frogOut(self):
        """
        Checks if the frog is offscreen.

        Once the frog is on the log, if it gets dragged beyond the width
        of the level's set width, it returns True.
        """
        if (self._frog != None and (self._frog.getX() > self.getWidth()*GRID_SIZE
            or self._frog.getX() <= 0)):
            return True

    def _keyLeft(self):
        """
        Sets the animator for when the frog moves left (the left arrow key
        is pressed).
        """
        dx = self._frog.getX()
        self._frog.setAngle(FROG_WEST)
        self._frog.animator = self._frog.animate_slideH('left',self.getWidth()*GRID_SIZE)
        next(self._frog.animator) # Start up the animator
        if self._containHedge(self._lanes) == True:
            self._frog.setX(dx)
            self._frog.animator = None

    def _keyRight(self):
        """
        Sets the animator for when the frog moves right (the right arrow key
        is pressed).
        """
        dx = self._frog.getX()
        self._frog.setAngle(FROG_EAST)
        self._frog.animator = self._frog.animate_slideH('right',self.getWidth()*GRID_SIZE)
        next(self._frog.animator) # Start up the animator
        if self._containHedge(self._lanes) == True:
            self._frog.setX(dx)
            self._frog.animator = None

    def _keyUp(self):
        """
        Sets the animator for when the frog moves up (the up arrow key
        is pressed).
        """
        dy = self._frog.getY()
        self._frog.setAngle(FROG_NORTH)
        self._frog.animator = self._frog.animate_slideV('up',self.getHeight()*GRID_SIZE)
        next(self._frog.animator) # Start up the animator
        if self._frog.getY()+ GRID_SIZE < (self.getHeight()*GRID_SIZE):
            dy += GRID_SIZE
            self._frog.setY(dy)
            if self._collision(self._lanes) == True:
                if self._containsExit(self._lanes) == True:
                    self._frog.setY(dy)
                    self._reachExit()
                    self._allOccupied = self._checkOccupied(self._lanes)
                elif self._containsOpening(self._lanes) == True:
                    self._frog.setY(dy-GRID_SIZE)
                else:
                    self._frog.setY(dy-GRID_SIZE)
                    self._frog.animator = None
            else:
                self._frog.setY(dy-+GRID_SIZE)
        else:
            self._frog.setY(dy)

    def _keyDown(self):
        """
        Sets the animator for when the frog moves down (the down arrow key
        is pressed).
        """
        dy = self._frog.getY()
        self._frog.setAngle(FROG_SOUTH)
        self._frog.animator = self._frog.animate_slideV('down',
                              self.getHeight()*GRID_SIZE)
        next(self._frog.animator) # Start up the animator
        if self._frog.getY() - GRID_SIZE > 0:
            dy -= GRID_SIZE
            self._frog.setY(dy)

            if self._collision(self._lanes) == True:
                if self._containsOpening(self._lanes) == True:
                    self._frog.setY(dy+GRID_SIZE)
                else:
                    self._frog.setY(dy+GRID_SIZE)
                    self._frog.animator = None
            else:
                self._frog.setY(dy+GRID_SIZE)
        else:
            self._frog.setY(dy)

    def _containHedge(self,lanes):
        """
        Checks if the frog is in Hedge Lane.

        Parameter lane: list of lanes in the level to loop through.
        Precondition: lanes is a list
        """
        for lane in lanes:
            if lane.getTile().source == 'hedge.png':
                if (self._frog != None and self._frog.getY() >= lane.getY()
                and self._frog.getY() <= lane.getY()+GRID_SIZE):
                    return True

    def _deadAnimate(self):
        """
        Starts the animation for the death sprite.

        Sets the position for the position at which the frog dies and
        starts the animation coroutine for the death sprite.
        """
        init_x = self._frog.getX()
        init_y = self._frog.getY()
        self._frog.visible = False
        self._deadfrog.visible = True
        self._deadfrog.x = init_x
        self._deadfrog.y = init_y
        self._deadfrog.animator = self._deadfrog.animate()
        next(self._deadfrog.animator) # Start up the animator
