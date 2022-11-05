from cmu_cs3_graphics import *
from .avatar import Avatar

class Student(Avatar):
    studentPositions = []
    def __init__(self, name):
        super().__init__(name)
        Student.studentPositions.append((self.left, self.top))

    def __repr__(self):
        return f'I am a student. My name is {self.name}.'