import Car

import pygame
import math

class HumanPlayer(Car):
    def __init__(self, window, dimensions, numCheckpoints, num, coords, colour, keys, startDegree, cosmetic, maxSpeed=10.4):
        super().__init__(window, dimensions, numCheckpoints, num, coords, colour, startDegree, maxSpeed, cosmetic)
        self.__rDown = False
        self.__lDown = False
        self.__keys = {"u" : keys[0], "d" : keys[1], "l" : keys[2], "r" : keys[3]}
        
    def drive(self):
        super().drive()
        left = pygame.key.get_pressed()[self.__keys["l"]]
        right = pygame.key.get_pressed()[self.__keys["r"]]
        if pygame.key.get_pressed()[self.__keys["u"]]:
            if self._currentSpeedPercent < 1:
                self._currentSpeedPercent += self._accel

        if pygame.key.get_pressed()[self.__keys["d"]]:
            if self._currentSpeedPercent > -1:
                self._currentSpeedPercent -= self._accel


        if self.canTurn():
            if not self.__lDown:
                if right:
                    self.__rDown = True
                    self._turnDirection = 1
                    self._movement(1)

                else:
                    self.__rDown = False

            if not self.__rDown:
                if left:
                    self.__lDown = True
                    self._turnDirection = -1
                    self._movement(-1)
                else:
                    self.__lDown = False

        if not self.canTurn() or (not left and not right):
            self._turnDirection = 0

    def lines(self, coeff):
        for change in range(1,480):
            y = -self._maxSpeed*math.cos(self._degree+(coeff*math.pi))*change*0.25 + self._coords[1]
            x = -self._maxSpeed*math.sin(self._degree+(coeff*math.pi))*change*0.25 + self._coords[0]
            pixels_array = pygame.PixelArray(self.window)
            try:
                if pixels_array[int(x), int(y)] == 4283016244:
                    break
            except:
                pass


        pixels_array.close()
        return x, y    

class AIPlayer(Car):
    def __init__(self, window, dimensions, numCheckpoints, num, coords, colour, startDegree, cosmetic=None, maxSpeed=10.4):
        super().__init__(window, dimensions, numCheckpoints, num, coords, colour, startDegree, maxSpeed, cosmetic)
    
    def drive(self):
        super().drive()
