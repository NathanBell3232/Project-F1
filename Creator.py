from Base import Base
from Track import Track
from TrackFinishLine import TrackFinishLine

import pygame
import time
import json

class Creator(Base):
    def __init__(self):
        super(Creator, self).__init__()
        blank_path = "tracks/pieces/piece_blank.png"
        self.__board = [[Track(blank_path) for x in range(6)] for y in range(4)]

        self.__pieces = self.getPngList("tracks/pieces/")
        self.__currentPiece = 0
        self.__errorTimer = 60
        self.__errorMessage = ""
        self.__hasFinishLine = False

        self.__buttonUp = pygame.Rect(1275, 0, 50, 50)
        self.__buttonDown = pygame.Rect(1275, 625, 50, 50)
        self.__buttonDone = pygame.Rect(1225, 715, 60, 40)
        self.__buttonExit = pygame.Rect(1315, 715, 60, 40)
        
        self.creatorScreen()

    def drawBoard(self):
        for y,row in enumerate(self.__board):
            for x,square in enumerate(row):
                image = self.window.blit(square.getImage(), (x*200, y*200))
                #Highlight box
                if image.collidepoint(self._mouse):
                    pygame.draw.rect(self.window, (255, 0, 0), [x*200, y*200, 200, 200], 5)
                    if self._leftClick:
                        path = f"tracks/pieces/{self.__pieces[self.__currentPiece]}"
                        if path.find("finish") > -1:
                            piece = TrackFinishLine(path)
                        else:
                            piece = Track(path)

                        if not piece.checkFinishLine():
                            if self.__board[y][x].checkFinishLine():
                                self.__hasFinishLine = False
                            self.__board[y][x] = piece

                        else:
                            if self.__board[y][x].checkFinishLine() or not self.__hasFinishLine:
                                self.__board[y][x] = piece
                                self.__hasFinishLine = True

                            elif not self.__board[y][x].checkFinishLine() and self.__hasFinishLine:
                                self.__resetErrorTimer("Only one finish line")

    def pieceOptions(self):
        for type, but in enumerate([self.__buttonUp, self.__buttonDown]):
            rotation = type*180
            button = pygame.draw.rect(self.window, (255,255,255), but)

            textRender = self.fontBig.render("^", True, (0,0,0))
            textRender = pygame.transform.rotate(textRender,rotation)
            self.window.blit(textRender, textRender.get_rect(center=but.center))

            if button.collidepoint(self._mouse) and self.click(0):
                if type == 0:
                    self.__currentPiece -=1
                else:
                    self.__currentPiece += 1

                self.__currentPiece %= len(self.__pieces)
        
        for coord, index in enumerate(range(self.__currentPiece-2,self.__currentPiece+3)):
            y = 75+(coord*110)
            index %= len(self.__pieces)
            piece = pygame.image.load(f"tracks/pieces/{self.__pieces[index]}")
            piece = pygame.transform.scale_by(piece, 0.4)
            self.window.blit(piece, (1260, y))
            if index == self.__currentPiece:
                pygame.draw.rect(self.window, (255, 0, 0), [1260, y, 80, 80], 4)
        
        done = pygame.draw.rect(self.window, (255,255,255), self.__buttonDone)
        textRender = self.fontSmall.render("DONE", True, (0,0,0))
        self.window.blit(textRender, textRender.get_rect(center=done.center))

        exit = pygame.draw.rect(self.window, (255,255,255), self.__buttonExit)
        textRender = self.fontSmall.render("EXIT", True, (0,0,0))
        self.window.blit(textRender, textRender.get_rect(center=exit.center))

        if done.collidepoint(self._mouse) and self.click(0):
            if not self.__hasFinishLine:
                self.__resetErrorTimer("Must have finish line")
            else:
                complete, coords = self.checkComplete()
                if complete:
                    self._running = False
                    self.screenshot(coords)

        elif exit.collidepoint(self._mouse) and self.click(0):
            self._running = False

    def checkComplete(self):
        found = False
        coords = []
        for y,row in enumerate(self.__board):
            if found:
                break

            for x,track in enumerate(row):
                if track.checkFinishLine():
                    track : TrackFinishLine
                    foundX,foundY = x, y
                    found = True
                    coords.append((foundX, foundY))
                    break

        prevDirection = track.getOrintation()
        #North
        if (prevDirection == 0):
            foundY -= 1
        #East
        elif (prevDirection == 1):
            foundX += 1
        #South
        elif (prevDirection == 2):
            foundY += 1
        #West
        else:
            foundX -= 1
            
        nextTrack = self.__board[foundY][foundX]
        directionDict = nextTrack.getDirections()
        index = "NESW"[(prevDirection + 2) % 4]

        direction = directionDict[index]
    
        if not direction:
            self.__resetErrorTimer("Finish line must connect to track")
            return False, None
        
        coords.append((foundX, foundY))    
        return self.recursiveCheck(foundX, foundY, prevDirection, coords)
        
    def recursiveCheck(self, x, y, prevDirection, coords):
        track = self.__board[y][x]
        if self.__board[y][x].checkFinishLine():
            return True, coords
        
        elif not (-1 < x < 6) or not (-1 < y < 4):
            self.__resetErrorTimer("Must be complete")
            return False, None

        directions = track.getDirections()
        for newDirection, direct in enumerate(directions):
            cardinalDirect = directions[direct]
            if (cardinalDirect and (prevDirection != (newDirection + 2) % 4)):
                coords.append((x, y))
                if (newDirection % 2) == 0:
                    y += [-1, 1][newDirection//2]
                else:
                    x += [1, -1][(newDirection-1)//2]

                return self.recursiveCheck(x, y, newDirection, coords)

        self.__resetErrorTimer("Must be complete")
        return False, None

    def screenshot(self, coords):
        square = Track("tracks/pieces/piece_blank.png")
        for y in range(4):
            for x in range(6):
                if ((x, y) not in coords):
                    self.window.blit(square.getImage(), (x*200, y*200))
        
        pygame.display.update()
        
        rect = pygame.Rect(0,0,1200,800)
        sub = self.window.subsurface(rect)
        tracks = self.getPngList("tracks/")
        #Name
        number = 0
        date = time.ctime()
        year = date[-4:]
        month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"].index(date[4:7]) + 1
        day = date[8:11]
        validName = False
        while not validName:
            try:
                self.__name = f"{year} {month} {day}_{number}"
                number += 1
                tracks.index(f"{self.__name}.png")
            except:
                validName = True

        pygame.image.save(sub, f"tracks/track_images/{self.__name}.png")
        self.__saveData(coords)

    def errorMessage(self):
        if self.__errorTimer != 60:
            textRender = self.fontBig.render(self.__errorMessage, True, (0,0,0))
            self.window.blit(textRender, textRender.get_rect(center=(600,400)))
            self.__errorTimer += 1
    
    def __resetErrorTimer(self, message):
        self.__errorMessage = message
        self.__errorTimer = 0

    def creatorScreen(self):
        while self._running:
            self._running = not self.quit()
            self.window.fill((73,164,52))
            self.registerInputs()
            self.drawBoard()
            self.pieceOptions()
            self.errorMessage()
            self.updateFrame(60)

    def __saveData(self, coords):
        boardData = []
        for j in range(4):
            row = []
            for i in range(6):
                spot = self.__board[j][i]
                directions = spot.getDirections()
                north, east, south, west = directions["N"], directions["E"], directions["S"], directions["W"]

                if ((i, j) not in coords):
                    integer = 0

                elif spot.checkFinishLine():
                    integer = 5
                    integer += spot.getOrintation()

                elif north and south:
                    integer = 1
                elif east and west:
                    integer = 2
                elif (north and east) or (south and west):
                    integer = 3
                elif (north and west) or (south and east):
                    integer = 4
                
                row.append(integer)

            boardData.append(row)

        trackData = self.__getDict()
        trackData[self.__name] = boardData

        json_object = json.dumps(trackData, indent=3)
        with open("tracks/trackData.json", "w") as outFile:
            outFile.write(json_object)

    def __getDict(self):
        #Try and read the dictionary file
        try:
            with open("tracks/trackData.json","r") as inFile:
                jsonFile = json.load(inFile)
            return jsonFile
        #If it has not been created yet, create it with an empty list
        except:
            with open("tracks/trackData.json","w") as outFile:
                outFile.write(json.dumps({}, indent=1))
            return {}
