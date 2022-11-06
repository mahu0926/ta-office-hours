from cmu_cs3_graphics import *
from .avatar import Avatar
import random

class Student(Avatar):
    studentPositions = []
    studentIndex = 0
    def __init__(self, name, qtype):
        super().__init__(name)
        self.label = 'Student'
        self.avatar = [ [0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [0, 0, 2, 2, 2, 2, 0, 0],
                        [0, 0, 0, 2, 2, 0, 0, 0],
                        [3, 3, 3, 3, 3, 3, 3, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 5, 0, 0, 5, 0, 0]]
        self.qtype = qtype
        self.colors = self.pickColors() + ['black']
        self.index = Student.studentIndex
        Student.studentPositions.append((self.left, self.top, self.index))
        Student.studentIndex += 1
    
    def setPosition(self, left, top):
        super().setPosition(left, top)
        Student.studentPositions[self.index] = (left,top,self.index)

    def onAppStart(self, app):
        app.stepsPerSecond = 1

    def move(self, app, left, top):
        while self.left != left and self.top != top:
            self.onStep(app)

    def onStep(self, app):
        self.left -= 1
        self.top -= 1

    def pickColors(self):
        colors = []
        for i in range(4):
            red = random.randrange(1,255)
            blue = random.randrange(1,255)
            green = random.randrange(1,255)
            colors.append(rgb(red, blue, green))
        return colors

    def chooseQuestion(self):
        if self.qtype == 'ct':
            print('code-tracinnnggg')
        elif self.qtype == 'conceptual':
            print('conceptualllll')
        elif self.qtype == 'freeresponse':
            print('freeeee responseeee')