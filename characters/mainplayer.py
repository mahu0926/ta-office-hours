from cmu_cs3_graphics import *
from .avatar import Avatar

class Main_Player(Avatar):

    def __init__(self, name):
        super().__init__(name)

    def __repr__(self):
        return f'I am the main bitch. My name is {self.name}.'
