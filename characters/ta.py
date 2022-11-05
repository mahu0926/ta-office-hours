from cmu_cs3_graphics import *
from .avatar import Avatar

class TA(Avatar):
    tapositions = []
    def __init__(self, name):
        super().__init__(name)
        TA.tapositions.append((self.left, self.top))

    def __repr__(self):
        return f'I am a TA. My name is {self.name}.'