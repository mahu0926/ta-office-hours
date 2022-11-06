from cmu_cs3_graphics import *
from characters.avatar import Avatar
from characters.student import Student
from characters.ta import TA
from characters.mainplayer import Main_Player
from characters.table import Table
import random

def onAppStart(app):
    app.message = None
    app.stepsPerSecond = 10
    app.width = 1200
    app.height = 800
    app.main_player = Main_Player('Grace', app.width/2, app.height/2)
    app.isInteracting = False
    app.students = []
    app.currStudent = None
    app.names = ['Jeremy', 'Lucy', 'James', 'Alice', 'Cathy', 'Janice', 'Louis'
                'Mahati', 'Archita', 'Andrea', 'Grace', 'Nick', 'Tracy', 'Fran',
                'Nasa', 'Bethany', 'Catherina', 'Sophia', 'Francesca', 'Darnell',
                'Gretchen', 'Gertrude', 'Geronimo', 'George', 'Gargantan', 'Hollie',
                'Lisa', 'Rose', 'Jennie', 'Jisoo']
    for i in range(6):
        name = app.names[random.randrange(0,len(app.names)-1)]
        app.students.append(Student(name))
        left = app.width/3-20 if i//3 == 0 else 2*app.width/3-20
        top = (app.height/2)-220+(150*(i%3))
        print(left, top)
        app.students[i].setPosition(left, top)
    
    app.queue = [(app.students[0].name, 'FRQ', 'Table 3')]

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

    for i in range(len(app.students)):
        app.students[i].drawItem()

    table1.drawItem()
    table2.drawItem()
    table3.drawItem()
    table4.drawItem()
    table5.drawItem()
    table6.drawItem()
    # print(app.main_player)

    if app.message != None:
        drawLabel(app.message, app.width/2, 650)


def onKeyHold(app, keys):
    print(app.main_player.disableIntersection())
    if not app.main_player.disableIntersection():
        app.main_player.move(keys)
    else:
        left, top, isLeft, isRight, isTop, isBottom = app.main_player.disableIntersection()
        app.currStudent = (left, top)
        if checkQueue(app, *app.currStudent):
            app.message = 'Press space to help the student'
        else:
            app.main_player.changeIntersection(isLeft, isRight, isTop, isBottom)
            app.message = 'Go help the first student in queue'
            app.currStudent = None

def checkQueue(app, left, top):
    queueName = app.queue[0][0]
    positions = Student.studentPositions
    studentIndex = positions.index((left, top))
    print(app.students[studentIndex].name, queueName)
    return app.students[studentIndex].name == queueName

def main():
    runApp()
main()