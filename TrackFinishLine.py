from Track import Track

class TrackFinishLine(Track):
    def __init__(self, path : str):
        super(TrackFinishLine, self).__init__(path)
        self.__orintation = self.__checkOrintation()

    def __checkOrintation(self):
        for index, chr in enumerate("URDL"):
            if self._path.find(chr) > -1:
                return index

    def checkFinishLine(self):
        return True
    
    def getOrintation(self):
        return self.__orintation