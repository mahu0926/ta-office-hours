from cmu_cs3_graphics import *

class Avatar:

    avatarPositions = []

    def __init__(self, name):
        self.avatar = []
        self.colors = []
        self.dims = (8, 20)
        self.name = name
        self.left = 0
        self.top = 0
        Avatar.avatarPositions.append((self.left, self.top))

    def __repr__(self):
        return f'I am a plain ass avatar. My name is {self.name}.'

    def setPosition(self, left, top):
        self.left = left
        self.top = top

    def getPosition(self):
        return self.left, self.top

    def move(self, key):
        if key == 'right': self.left += 10
        elif key == 'left': self.left -= 10
        if key == 'up': self.top -= 10
        elif key == 'down': self.top += 10
