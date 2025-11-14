import numpy as np
class greedSearchFunc:
    def __init__(self, position = ()):
        self.starting = position
        self.distance = 0


    def addDistane(self, val):
        self.distance = self.distance + val

    def getPos(self):
        return self.starting
