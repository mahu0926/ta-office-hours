from cmu_cs3_graphics import *
from characters.avatar import Avatar

from characters.student import Student
from characters.ta import TA
from characters.mainplayer import Main_Player

def redrawAll(app):
    mahati = Avatar('mahati')
    grace = Main_Player('grace')
    alice = Student('alice')
    andrea = TA('andrea')
    print(mahati)
    print(grace)
    print(alice)
    print(andrea)

def main():
    runApp()
main()