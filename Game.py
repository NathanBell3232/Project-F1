from Base import Base
from Palette import Palette
from Players import HumanPlayer, AIPlayer

import math
import pygame
import random
import json

class Game(Base):
    def __init__(self, player_number, path):
        super(Game, self).__init__()
        self.__playerNum = player_number
        self.__track = pygame.image.load(f"tracks/track_images/{path}").convert()
        self.__checkpoints, self.__finishLine, self.__flOrientation = self.extractCheckpoints(path[:-4])
        self.__carsList = []
        self.__paletteList = self.makePaletteList()
        self.__gameMusic = pygame.mixer.Sound("music/Telephonesis.wav")
        self.startGame()

    def makePaletteList(self):
        paletteList = []
        with open("cars/carData.json", "r") as inFile:
            file = json.load(inFile)
            
        for count in range(self.__playerNum):
            data = file[f"Car{count+1}"]
            coords = [80+(550*count), 75]
            paletteList.append(Palette(count+1, coords, data["num"],
                                        data["cosNum"], data["colour"]))
        
        return paletteList

    def make_players(self, num):
        allControls = [[pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d],
                        [pygame.K_i, pygame.K_k, pygame.K_j, pygame.K_l]]
        carsList = []
        for count in range(num):
            colour = self.__paletteList[count].getColour()
            cosmetic = self.__paletteList[count].getCosmetic()
            numCheckpoints = 0
            for check in self.__checkpoints:
                if (check is not None):
                    numCheckpoints += 1
                    
            topLeftCoord = self.__finishLine[0][0]//200, self.__finishLine[0][1]//200
            degreeX, degreeY = 0, 0
            if (self.__flOrientation == 0):
                degreeX = 70+(60*((count)%2))
                degreeY = 100
            elif (self.__flOrientation == 1):
                degreeX = 100
                degreeY = 70+(60*((count)%2))
            elif (self.__flOrientation == 2):
                degreeX = 130-(60*((count)%2))
                degreeY = 100
            else:
                degreeX = 100
                degreeY = 130-(60*((count)%2))
                
            coords = [degreeX+(topLeftCoord[0]*200), degreeY+(topLeftCoord[1]*200)]
            
            carsList.append(HumanPlayer(self.window, (self._width, self._height),numCheckpoints, count+1, coords, colour, 
                                        allControls[count], -((self.__flOrientation)/2)*math.pi, cosmetic))

        return carsList

    def extractCheckpoints(self, path):
        with open("tracks/trackData.json") as inFile:
            js = json.load(inFile)
            
        trackData = js[path]
        
        fLineNorth = [[0, 50], [200, 50]]
        fLineEast = [[140, 0], [140, 200]]
        fLineSouth = [[0, 145], [175, 200]]
        fLineWest = [[60, 0], [60, 200]]

        finishLine = None
        checkpoints = []
        for i in range(4):
            for j in range(6):
                spot = trackData[i][j]
                #If blank
                if (spot == 0):
                    trackObj = None
                #Else if normal track piece
                else:
                    if (spot < 5):
                        trackObj = [[[0, 100], [200, 100]], [[100, 0], [100, 200]], 
                                    [[0, 200], [200, 0]], [[0, 0], [200, 200]]][spot-1]
                    #Else finish line
                    else:
                        trackObj = [fLineNorth, fLineEast, fLineSouth, fLineWest][spot-5]
                        finishLine = trackObj
                        flOrientation = spot-5
                        
                    for k in range(2):
                        trackObj[k][0] += j*200
                        trackObj[k][1] += i*200
                        
                checkpoints.append(trackObj)

        return checkpoints, finishLine, flOrientation

    def __startLights(self, i=None):
        rectangle = pygame.Rect(350, 350, 500, 100)
        pygame.draw.rect(self.window, (63, 63, 63),rectangle)
        for count in range(5):
            if i is None:
                colour = (40,40,40)
            elif count <= i and i != 5:
                colour = (255,0,0)
            else:
                if i == 5:
                    time = random.randint(200,500)
                    while (time != 0):
                        pygame.time.delay(1)
                        time -= 1
                        if (self.quit):
                            break
                    
                colour = (40,40,40)

            pygame.draw.circle(self.window, colour, [400+(100*count), 400], 30, 0)

    def startGame(self):
        self.window.fill((73,164,52))
        start_message = self.fontBig.render(f"Press space to start", True, (0,0,0))
        self.window.blit(start_message, start_message.get_rect(center=(600,750)))
        pygame.display.update()
        
        controls = ["WASD", "IJKL"]
        end = False
        while not pygame.key.get_pressed()[pygame.K_SPACE] and not end:
            for index,pal in enumerate(self.__paletteList):
                pal.draw(True)
                pal.change_colour()

                controlsText = self.fontBig.render(controls[index], True, (0,0,0))
                point = pal.getMidpoint()
                self.window.blit(controlsText, controlsText.get_rect(center=(point[0],point[1]+150)))

            self.updateFrame(60)
            end = self.quit()
        
        for pal in self.__paletteList:
            pal.screenshot()
    
        self.__carsList = self.make_players(self.__playerNum)

        if not end:
            self.window.blit(self.__track, (0,0))
            for car in self.__carsList:
                car.draw()

        for i in range(6):
            if self.quit() or end:
                self._running = False
                end = True
                break
            
            self.__startLights(i)
            if i != 5:
                self.updateFrame(1)
                
        if not end:
            self.__gameMusic.play(-1)

        winner = self.fontBig.render("No one", True, (0,0,0))
        while self._running and not end:
            #Quit the game
            self._running = not self.quit()
            
            self.window.fill((73,164,52))
            self.window.blit(self.__track, (0,0))
            for car in self.__carsList:
                car.drive()
                car.setLapTime(False)
                tempIndex = -1
                for check in self.__checkpoints:
                    if (check is not None):
                        tempIndex += 1
                        checkpointDrawn = pygame.draw.line(self.window, (0,0,255), check[0], check[1], 20)
                        if (checkpointDrawn.collidepoint(car.getCoords())):
                            if (check != self.__finishLine):
                                car.setCheckpoints(tempIndex)
                                
                            else:
                                numFalse = 0
                                for checkBool in car.getCheckpoints():
                                    if (not checkBool):
                                        numFalse += 1
                                if (numFalse <= 1):
                                    car.setCheckpoints(tempIndex)

            # draw the track to remove checkpoint lines
            self.window.fill((73,164,52))
            self.window.blit(self.__track, (0,0))
            for index, car in enumerate(self.__carsList):
                carLapCount = car.getLapCount()
                if car.checkEndLap():
                    car.setLapTime(True)
                    

                numberCar = self.fontBig.render(controls[index], True, car.getColour())
                self.window.blit(numberCar, numberCar.get_rect(center=(350+(250*(car.getNumber()-1)), 200)))

                for num, time in enumerate(car.getLapTimes()[:carLapCount]):
                    time = self.fontBig.render(str(round(time, 3)), True, (0,0,0))
                        
                    coordX = 350+(250*(car.getNumber()-1))
                    coordY = 250 + (num*50)

                    self.window.blit(time, time.get_rect(center=(coordX, coordY)))

                carLapText = self.fontBig.render(f"Car {car.getNumber()} Lap {carLapCount}/7 ", True, (0,0,0))
                self.window.blit(carLapText, ((975*(car.getNumber()-1), 0)))

                if car.getLapCount() == 7 and self._running:
                    winner = self.fontBig.render(f"Car {car.getNumber()} wins!", True, (0,0,0))
                    self._running = False
                
                car.draw()
                # draw the lines used for AI (currently unused)
                '''for coeff in range(-4, 5):
                    coeff *= 0.125
                    tuple = car.lines(coeff)
                    pygame.draw.line(self.window, (0,0,0), car.getCoords(), (tuple))'''
                
            self.updateFrame(60)
            
        if not end:
            self.__gameMusic.fadeout(1500)
            self.window.fill((73,164,52))
            self.window.blit(self.__track, (0,0))
            self.window.blit(winner, winner.get_rect(center=(600,350)))

            textTime = self.fontBig.render("Fastest times", True, (0,0,0))
            self.window.blit(textTime, textTime.get_rect(center=(600, 400)))
            for index, car in enumerate(self.__carsList):
                if car.getLapCount() > 0:
                    fastest = str(car.getFastestTime())
                else:
                    fastest = "N/A"

                textFastest = f"{controls[index]}: " + fastest
                textFastest = self.fontBig.render(textFastest, True, car.getColour())
                coords = [350 + (500*(index%2)),450+(50*(index//2))]
                self.window.blit(textFastest, textFastest.get_rect(center=coords))

            endMessage = self.fontBig.render(f"Press space to end", True, (0,0,0))
            self.window.blit(endMessage, endMessage.get_rect(center=(600,585)))

            while not pygame.key.get_pressed()[pygame.K_SPACE]:
                self.updateFrame(60)
                for event in pygame.event.get():
                    pass