
import abc
import math
import pygame
import time

class Car(metaclass=abc.ABCMeta):
    def __init__(self, window, dimensions, numCheckpoints, num, coords, colour, startDegree, maxSpeed, cosmetic):
        self.window = window
        self._windowWidth, self._windowHeight = dimensions
        self._checkpoints = [False for count in range(numCheckpoints)]
        self._lapCount = 0
        self._lapTimes = [-1 for count in range(7)]
        self._degree = startDegree
        self._turnDirection = 0
        self._grass = False

        self._image = pygame.image.load(f"cars/car{num}.png").convert()
        self._image = pygame.transform.scale_by(self._image, 1/3)
        self._image.set_colorkey((73,164,52))
        self._cosmetic = cosmetic
        if self._cosmetic != None:
            self._cosmetic = pygame.image.load(f"cosmetics/{self._cosmetic}").convert()
            self._cosmetic.set_colorkey((73,164,52))

        self._coords = coords
        if (startDegree == -1/2*math.pi):   
            self._vector = [maxSpeed,0]
        elif (startDegree == -math.pi):
            self._vector = [0,maxSpeed]
        elif (startDegree == -3/2*math.pi):
            self._vector = [-maxSpeed,0]
        else:
            self._vector = [0,-maxSpeed]

        self._carNumber = num
        self._colour = colour
        self._maxSpeed = maxSpeed
        self._accel = 0.01
        self._currentSpeedPercent = 0
        self._tireFriction = 0.72

        self.draw()

    def draw(self):
        image = pygame.transform.rotate(self._image, round((self._degree*57), 2))
        carRect = image.get_rect()
        carRect.center = self._coords
        self.window.blit(image, carRect)

        #Tires math.tan(12/14)
        if self._turnDirection == 0:
            extra = 0
        else:
            extra = -math.pi/4 * self._turnDirection

        tire = pygame.Surface((7,9))
        tire.set_colorkey((0,0,0))
        tire.fill((1,1,1))
        degree = math.tan(12/14)/2
        length = math.hypot(11, 14)
        for coeff in [-1, 1]:
            y = -length*math.cos(self._degree+(coeff*degree)) + self._coords[1]
            x = -length*math.sin(self._degree+(coeff*degree)) + self._coords[0]
            new_tire = pygame.transform.rotate(tire, round((extra+self._degree)*57, 2))
            tireRect = new_tire.get_rect()
            tireRect.center = (x, y)
            self.window.blit(new_tire, tireRect)
        
        if self._cosmetic != None:
            cosRect = self._cosmetic.get_rect()
            cosRect.center = self._coords
            self.window.blit(self._cosmetic, cosRect)

    def resetCheckpoints(self):
        self._checkpoints = [False for i in range(len(self._checkpoints))]

    def setCheckpoints(self, index : int):
        self._checkpoints[index] = True

    def checkEndLap(self):
        for check in self._checkpoints:
            if not check:
                return False

        self._lapCount += 1
        self.resetCheckpoints()
        return True

    def _movement(self, coeff : int):
        self._degree -= self.__getDegreeTurn(coeff)
        self._degree %= 2*math.pi
        self._vector[0] = -self._maxSpeed*math.sin(self._degree)
        self._vector[1] = -self._maxSpeed*math.cos(self._degree)

    
    def __getDegreeTurn(self, coeff : int):
        return (((1/60)*9.81*self._tireFriction*2)/(self._maxSpeed*self._currentSpeedPercent))*coeff
    
    def __checkOnTrack(self):
        pixels_array = pygame.PixelArray(self.window)
        if pixels_array[self._coords[0], self._coords[1]] == 4283016244:
            self._grass = True
        else:
            self._grass = False

        pixels_array.close()

    def setLapTime(self, end : bool):
        if not end:
            if self._lapTimes[self._lapCount] == -1:
                self._lapTimes[self._lapCount] = time.time()
        else:
            self._lapTimes[self._lapCount-1] = time.time() - self._lapTimes[self._lapCount-1]
    
    def drive(self):
        if self._coords[0] < 5:
            self._coords[0] = 5
        elif self._coords[0] > self._windowWidth-20:
            self._coords[0] = self._windowWidth-20

        if self._coords[1] < 5:
            self._coords[1] = 5
        elif self._coords[1] > self._windowHeight-20:
            self._coords[1] = self._windowHeight-20

        self._coords[0] += int(self._vector[0]*self._currentSpeedPercent)
        self._coords[1] += int(self._vector[1]*self._currentSpeedPercent)
        
        #Driving on track
        self.__checkOnTrack()
        self._drag()

    def _drag(self):
        #Wind resistance
        #Travelling forwards
        if self._currentSpeedPercent > 0:
            self._currentSpeedPercent -= self._accel*0.5
        #Travelling backwards
        elif self._currentSpeedPercent < 0:
            self._currentSpeedPercent += self._accel*0.5

        #Collision with grass
        if self._grass:
            if self._currentSpeedPercent > 0.5:
                self._currentSpeedPercent -= self._accel*1.5
            elif self._currentSpeedPercent < -0.5:
                self._currentSpeedPercent += self._accel*1.5
            self._tireFriction = 0.35
        else:
            self._tireFriction = 0.72
    
    def canTurn(self):
        return round(abs(self._currentSpeedPercent), 1) > 0.1
    
    def getCoords(self):
        return self._coords

    def getColour(self):
        return self._colour
    
    def getNumber(self):
        return self._carNumber

    def getCheckpoints(self):
        return self._checkpoints
        
    def getLapTimes(self):
        return self._lapTimes
    
    def getFastestTime(self):
        for time in sorted(self._lapTimes):
            if (time != -1):
                return round(time, 3)
    
    def getLapCount(self):
        return self._lapCount