from cmu_cs3_graphics import *

class Avatar:

    avatarPositions = []
    pixelsize = 5

    def __init__(self, name='Untitled'):
        self.avatar = []
        self.colors = []
        self.dims = (8, 20)
        self.name = name
        self.left = 0
        self.top = 0
        Avatar.avatarPositions.append((self.left, self.top))
        self.label = 'avatar'

    def __repr__(self):
            return f'I am a {self.label}. My name is {self.name}.'

    def setPosition(self, left, top):
        self.left = left
        self.top = top

    def getPosition(self):
        return self.left, self.top

    def move(self, keys):
        if 'right' in keys: self.left += 10
        elif 'left' in keys: self.left -= 10
        if 'up' in keys: self.top -= 10
        elif 'down' in keys: self.top += 10

    def getPixelLeftTop(self, row, col):
        left, top = (self.left, self.top)
        left = left + col * Avatar.pixelsize
        top = top + row * Avatar.pixelsize
        return left, top

    def drawItem(self):
        item = self.avatar
        print(item)
        colors = self.colors
        left, top = (self.left, self.top)
        rows, cols = len(item), len(item[0])
        for row in range(rows):
            for col in range(cols):
                if item[row][col] != 0:
                    color = colors[item[row][col]-1]
                else:
                    color = None
                pixelLeft, pixelTop = self.getPixelLeftTop(row, col)
                drawRect(pixelLeft, pixelTop, Avatar.pixelsize, Avatar.pixelsize,
                        fill=color)

