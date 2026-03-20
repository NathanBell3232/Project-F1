from os import listdir
from os.path import isfile, join

import abc
import pygame

class Base(metaclass=abc.ABCMeta):
    def __init__(self):
        self._width = 1400
        self._height = 800
        self.window = pygame.display.set_mode((self._width,self._height))
        self.fontBig = pygame.font.SysFont("Corbel.ttf", 50)
        self.fontSmall = pygame.font.SysFont("Corbel.ttf", 30)
        self._clock = pygame.time.Clock()

        self._leftClick, self._rightClick = False, False
        self._leftDown, self._rightDown = False, False
        self._mouse = (0,0)
        self._running = True
    
    def registerInputs(self):
        self._leftClick = pygame.mouse.get_pressed()[0]
        self._rightClick = pygame.mouse.get_pressed()[2]
        self._mouse = pygame.mouse.get_pos()

    def click(self, type=int):
        if type == 0:
            if self._leftClick and not self._leftDown:     
                self._leftDown = True
                return True
            elif not self._leftClick:
                self._leftDown = False
        else:
            if self._rightClick and not self._rightDown:     
                self._rightDown = True
                return True
            elif not self._rightClick:
                self._rightDown = False

        return False
    
    def quit(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True

        return False

    def updateFrame(self, frame : int):
        pygame.display.update()
        self._clock.tick(frame)
        
    def getPngList(self, path):
        pngList = [f for f in listdir(path) if isfile(join(path, f)) if f.find(".png") > -1]
        return sorted(pngList)
