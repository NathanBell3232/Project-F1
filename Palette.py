import Base

import pygame
import random
import json

class Palette(Base):
    def __init__(self, carNum, coords, num, cosNum, colour):
        super(Palette, self).__init__()
        self.__carNum = carNum
        self.__cosList = [None] + self.getPngList("cosmetics/")
        self.__cosNumber = cosNum

        self.__x, self.__y = coords
        self.__colourStep = 10
        self.__boxWidth = int(25*1.5)
        self.__colour = colour
        self.__width = self.__colourStep*self.__boxWidth

        self.__squareColour = pygame.Rect(self.__x+self.__width,self.__y,self.__boxWidth*3,self.__boxWidth*3)
        self.__squareBig = pygame.Rect(self.__x,self.__y+(3*self.__boxWidth),self.__width,self.__width)
        self.__cosButtonUp = pygame.Rect(self.__x+self.__width+self.__boxWidth,self.__y+self.__boxWidth*3,
                                           self.__boxWidth,self.__boxWidth)
        self.__cosButtonDown = pygame.Rect(self.__x+self.__width+self.__boxWidth,self.__y + self.__boxWidth*13,
                                           self.__boxWidth,self.__boxWidth)

        
        self.__car = pygame.image.load(f"cars/car_blank copy.png").convert()
        self.__car = pygame.transform.scale_by(self.__car, 3)
        self.__car.set_colorkey((255,64,255))
        ######
        self.__tires = pygame.Surface((21, 30))

        self.__shade = pygame.image.load(f"cars/car_blank_shade.png").convert()
        self.__shade = pygame.transform.scale_by(self.__shade, 3)
        self.__shade.set_colorkey((255,64,255))
        self.__shade.set_alpha(51)

        self.__num = num

    def draw(self, drawTire):
        #Draw the colours
        for y in range(3):
            for x in range(self.__colourStep):
                coordX = self.__x+(x*self.__boxWidth)
                coordY = self.__y+(y*self.__boxWidth)
                square = pygame.Rect(coordX,coordY,self.__boxWidth,self.__boxWidth)
                col = (255/(self.__colourStep))*(x+1)
                if y == 0:
                    currentColour = (col,self.__colour[1],self.__colour[2])
                elif y == 1:
                    currentColour = (self.__colour[0],col,self.__colour[2])
                else:
                    currentColour = (self.__colour[0],self.__colour[1],col)

                pygame.draw.rect(self.window, currentColour, square)

            colourX = (self.__width*(self.__colour[y]/255) - (self.__boxWidth//2)-4)//1
            whiteRect = pygame.Rect(self.__x+colourX,self.__y+(y*self.__boxWidth),7,self.__boxWidth)
            pygame.draw.rect(self.window, (255,255,255), whiteRect)
        
        #Draw the two squares
        pygame.draw.rect(self.window, self.__colour, self.__squareColour)
        pygame.draw.rect(self.window, self.__colour, self.__squareBig)

        #Draw the car
        pointCar = (self.__x, self.__y+(self.__boxWidth*3))
        car = self.window.blit(self.__car, pointCar)
        self.window.blit(self.__shade, pointCar)

        if drawTire:
            #Draw the wheels
            pointWheel = [car.center[0], car.center[1]]
            pointWheel[1] -= 43
            for x in range(2):
                pointWheel[0] += (x*99)-33
                self.window.blit(self.__tires, self.__tires.get_rect(center=pointWheel))

        #Draw the numbers
        imageNumbers = pygame.image.load(f"cars/numbers.png").convert()
        numberCar = imageNumbers.subsurface((9*self.__num, 0), (9,9))
        for i in range(2):
            if i == 0:
                numberCar = pygame.transform.scale_by(numberCar, 3)
                pointNumber = self.__car.get_rect().center
                pointNumber = pointNumber[0]+self.__x, pointNumber[1]+self.__y+66
            else:
                numberCar = pygame.transform.scale_by(numberCar, 3)
                
                pointNumber = self.__squareColour.center

            numberCar.set_colorkey((255,64,255))
            self.window.blit(numberCar, numberCar.get_rect(center=pointNumber))
        #######Hacker rank
        #Draw the cosmetics
        self.drawCosmetics()
        
        
    def drawCosmetics(self):
        reset = pygame.Rect(self.__x+self.__width,self.__y+self.__boxWidth*3, self.__boxWidth*3.5, 125*3)
        pygame.draw.rect(self.window, (73,164,52), reset)
        for type,box in enumerate([self.__cosButtonUp, self.__cosButtonDown]):
            if type == 0:
                rotation = 0
            else:
                rotation = 180

            textRender = self.fontBig.render("^", True, (0,0,0))
            textRender = pygame.transform.rotate(textRender,rotation)

            pygame.draw.rect(self.window, (255,255,255), box)
            self.window.blit(textRender, textRender.get_rect(center=box.center))
        
        for num, index in enumerate(range(self.__cosNumber-1, self.__cosNumber+2)):
            cosPointY = self.__y + self.__boxWidth*6 + num*100
            index %= len(self.__cosList)
            cosName = self.__cosList[index]
            if cosName != None:
                cos = pygame.image.load(f"cosmetics/{cosName}").convert()
                cos = pygame.transform.scale_by(cos, 3-0.5)
                cos.set_colorkey((73,164,52))
                if index != self.__cosNumber:
                    cos.set_alpha(100)
                
                self.window.blit(cos, cos.get_rect(center=(box.center[0], cosPointY)))
    
    def change_colour(self):
        pos = pygame.mouse.get_pos()
        self._leftClick = pygame.mouse.get_pressed()[0]
        self._rightClick = pygame.mouse.get_pressed()[2]
        
        indexY = (pos[1]-self.__y)//self.__boxWidth
        if -1 < indexY < 3:
            if -1 < pos[0]-self.__x <= self.__width-1:
                #Colour wheel
                if self._leftClick:
                    self.__colour[indexY] = (((pos[0]-self.__x)//self.__boxWidth)/self.__colourStep)*255+25.5
                    self._leftDown = True
            
            elif -1 < pos[0]-self.__x-self.__width < self.__boxWidth*3:
                if self.click(0):
                    self.__num += 1
                    self.__num %= 10

                #Random colour
                if self.click(1):
                    self.randomColour()

        elif pygame.mouse.get_pressed()[1]:
            if -1 < indexY < 3:
                if -1 < pos[0]-self.__x <= self.__width-1:
                    self.__colour[indexY] = (((pos[0]-self.__x)//self.__boxWidth)/self.__colourStep)*255
        else:
            #Cosmetic
            for type,box in enumerate([self.__cosButtonUp, self.__cosButtonDown]):
                box = pygame.draw.rect(self.window, (255,255,255), box)
                if box.collidepoint(pos):
                    if self.click(0):
                        if type == 0:
                            self.__cosNumber-= 1
                            if self.__cosNumber == -1:
                                self.__cosNumber = len(self.__cosList)-1
                        else:
                            self.__cosNumber+= 1
                        self.__cosNumber%= len(self.__cosList)

        self.drawCosmetics()
    
    def randomColour(self):
        self.__colour = [(random.randint(1,self.__colourStep)*(255/self.__colourStep)) for count in range(3)]

    def getColour(self):
        return self.__colour
    
    def getMidpoint(self):
        width = self.__width
        return [self.__x+(width//2), self.__y+(width//2)+(self.__boxWidth*3)]
    
    def getNumber(self):
        return self.__num
    
    def getCosmetic(self):
        return self.__cosList[self.__cosNumber]
    
    def screenshot(self):
        self.draw(False)
        rect = pygame.Rect(self.__x+90,self.__y+(self.__boxWidth*3)+90,195,195)
        sub = self.window.subsurface(rect)
        pygame.image.save(sub, f"cars/car{self.__carNum}.png")
        
        self.savePalette()
        
    def savePalette(self):
        carDict = {}
        carDict["num"] = self.__num
        carDict["cosNum"] = self.__cosNumber
        carDict["colour"] = self.__colour
        
        with open("cars/carData.json", "r") as inFile:
            file = json.load(inFile)
        file[f"Car{self.__carNum}"] = carDict
    
        with open("cars/carData.json", "w") as outFile:
            json.dump(file, outFile, indent=1)
    
    def resetPalette(num):
        carDict = {}
        carDict["num"] = 0
        carDict["cosNum"] = 0
        carDict["colour"] = [25.5, 25.5, 25.5]
        
        with open("cars/carData.json", "r") as inFile:
            file = json.load(inFile)
        file[f"Car{num}"] = carDict
    
        with open("cars/carData.json", "w") as outFile:
            json.dump(file, outFile, indent=1)
