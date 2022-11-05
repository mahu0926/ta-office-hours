from cmu_cs3_graphics import *
from characters.avatar import Avatar
from characters.student import Student
from characters.ta import TA
from characters.mainplayer import Main_Player
from characters.table import Table

def onAppStart(app):
    app.main_player = Main_Player('Grace')
    app.stepsPerSecond = 10
    app.width = 1200
    app.height = 800

    app.stud1 = Student('Jeremy')
    app.stud2 = Student('Mia')
    app.stud3 = Student('Mia')
    app.stud4 = Student('Mia')
    app.stud5 = Student('Mia')
    app.stud6 = Student('Mia')

    app.stud1.setPosition(app.width/3-20, app.height/2-220)
    app.stud2.setPosition(app.width/3-20, app.height/2-70)
    app.stud3.setPosition(app.width/3-20, app.height/2+80)
    app.stud4.setPosition(2*app.width/3-20, app.height/2-220)
    app.stud5.setPosition(2*app.width/3-20, app.height/2-70)
    app.stud6.setPosition(2*app.width/3-20, app.height/2+80)

def redrawAll(app):
    app.main_player.drawItem()

    table1 = Table()
    table2 = Table()
    table3 = Table()
    table4 = Table()
    table5 = Table()
    table6 = Table()


    table1.setPosition(app.width/3-50, app.height/2-150)
    table2.setPosition(app.width/3-50, app.height/2)
    table3.setPosition(app.width/3-50, app.height/2+150)
    table4.setPosition(2*app.width/3-50, app.height/2-150)
    table5.setPosition(2*app.width/3-50, app.height/2)
    table6.setPosition(2*app.width/3-50, app.height/2+150)

    app.stud1.drawItem()
    app.stud2.drawItem()
    app.stud3.drawItem()
    app.stud4.drawItem()
    app.stud5.drawItem()
    app.stud6.drawItem()

    table1.drawItem()
    table2.drawItem()
    table3.drawItem()
    table4.drawItem()
    table5.drawItem()
    table6.drawItem()
    # print(app.main_player)

def onKeyHold(app, keys):
    app.main_player.move(keys)

def main():
    runApp()
main()