from cmu_cs3_graphics import *
from .avatar import Avatar
import random

class Student(Avatar):
    studentPositions = []
    studentIndex = 0
    def __init__(self, name):
        super().__init__(name)
        Student.studentPositions.append((self.left, self.top))
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
        self.colors = self.pickColors() + ['black']
        self.index = Student.studentIndex
        Student.studentIndex += 1
    
    def setPosition(self, left, top):
        super().setPosition(left, top)
        Student.studentPositions[self.index] = (left,top)

    def pickColors(self):
        colors = []
        for i in range(4):
            red = random.randrange(1,255)
            blue = random.randrange(1,255)
            green = random.randrange(1,255)
            colors.append(rgb(red, blue, green))
        return colors

