import pygame

class Track():
    def __init__(self, path : str):
        self._path = path
        self._directions = self.__makeDirectionsDict()

    def __makeDirectionsDict(self):
        cardinalDirections = {"N":False, "E":False, "S":False, "W":False}
        dir = self._path.split("/")[-1]
        dir = dir.split("_")[-1][:-4]
        if (dir.lower() != "blank"):   
            for letter in dir:
                cardinalDirections[letter] = True

        return cardinalDirections

    def getImage(self):
        return pygame.image.load(self._path).convert()
    
    def getDirections(self):
        return self._directions

    def checkFinishLine(self):
        return False