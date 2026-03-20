import Base
import Creator
import Game
import Palette

import os
import pygame
import json

class TrackSelector(Base):
    def __init__(self):
        super(TrackSelector, self).__init__()
        self.__tracks = self.getPngList("tracks/")
        self.__buttonLeft = pygame.Rect(400, 675, 50, 50)
        self.__buttonRight = pygame.Rect(750, 675, 50, 50)
        self.__buttonDelete = pygame.Rect(1215, 500, 170, 50)
        self.__buttonConfirm = pygame.Rect(1215, 700, 170, 50)

        self.__startTrack = 0
        self.__currentTrack = -1
        
        self.selectTrack()

    def selectTrack(self):
        while self._running:
            self._running = not self.quit()
            self.window.fill((73,164,52))
            self.registerInputs()
            #Tracks selector
            for index in range(self.__startTrack, self.__startTrack+6):
                try:
                    track = pygame.image.load("tracks/" + self.__tracks[index]).convert()
                except:
                    continue
                track = pygame.transform.scale_by(track, 1/4)
                
                displaindexY = index%6
                y = 100+(displaindexY//3)*300
                x = 50+(displaindexY%3)*400
                track = self.window.blit(track, (x,y))
                if track.collidepoint(self._mouse):
                    pygame.draw.rect(self.window, (255, 0, 0), [x, y, 300, 200], 4)
                    if self.click(0):
                        if index != len(self.__tracks)-1:
                            self.__currentTrack = index
                        else:
                            Creator()
                            self.__tracks = self.getPngList("tracks/")
                
                if index == self.__currentTrack:
                    pygame.draw.rect(self.window, (0, 255, 0), [x, y, 300, 200], 4)
                        
            
            #Track page buttons
            for type, button in enumerate([self.__buttonLeft, self.__buttonRight]):
                button = pygame.draw.rect(self.window, (255,255,255), button)

                textRender = self.fontBig.render("<>"[type], True, (0,0,0))
                self.window.blit(textRender, textRender.get_rect(center=button.center))
                if button.collidepoint(self._mouse) and self.click(0):
                    if type == 0 and self.__startTrack > 0:
                        self.__startTrack -= 6

                    elif type == 1 and self.__startTrack < len(self.__tracks)-6:
                        self.__startTrack += 6

            if self.__currentTrack > -1:
                text = self.__tracks[self.__currentTrack]
                textRender = self.fontBig.render(text[:-4], True, (0,0,0))
                self.window.blit(textRender, textRender.get_rect(center=(600, button.center[1])))

            #Confirm button
            buttonConfirm = pygame.draw.rect(self.window, (255,255,255), self.__buttonConfirm)
            textRender = self.fontBig.render("CONFIRM", True, (0,0,0))
            self.window.blit(textRender, textRender.get_rect(center=buttonConfirm.center))
            if buttonConfirm.collidepoint(self._mouse) and self.__currentTrack != -1 and self.click(0):
                #import track into match
                Game(2, self.__tracks[self.__currentTrack])
            
            #Delete button
            buttonDelete = pygame.draw.rect(self.window, (255,255,255), self.__buttonDelete)
            textRender = self.fontBig.render("DELETE", True, (0,0,0))
            self.window.blit(textRender, textRender.get_rect(center=buttonDelete.center))
            if buttonDelete.collidepoint(self._mouse) and self.__currentTrack != -1 and self.click(0):
                os.remove(os.path.join("tracks/", text))
                
                with open("tracks/trackData.json", "r") as infile:
                    file = json.load(infile)
                file.pop(text[:-4])
                with open("tracks/trackData.json", "w") as outFile:
                    json.dump(file, outFile, indent=1)

                self.__currentTrack = -1
                self.__tracks = self.getPngList("tracks/")

            self.updateFrame(60)

        for i in range(1,3):
            Palette.resetPalette(i)
