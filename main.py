from cmu_cs3_graphics import *
from characters.avatar import Avatar
from characters.student import Student
from characters.ta import TA
from characters.mainplayer import Main_Player
from characters.table import Table
from codeTracing import CodeTracing
import random

def onAppStart(app):
    app.message = 'Go help the first student in queue'
    app.stepsPerSecond = 10
    app.width = 1200
    app.height = 800
    app.main_player = Main_Player('Grace', app.width/2, app.height/2)
    app.isInteracting = False
    app.numStudents = 6
    app.currStudent = None
    app.selectedQuestion = None
    app.queuePosition = 0
    app.score = 0
    
    studentsAndTablesAndQueue(app)
    CodeTracing.loadCodeTracings(app)

def studentsAndTablesAndQueue(app):
    app.students = []
    app.tables = []
    app.names = ['Jeremy', 'Lucy', 'James', 'Alice', 'Cathy', 'Janice', 'Louis'
                'Mahati', 'Archita', 'Andrea', 'Grace', 'Nick', 'Tracy', 'Fran',
                'Nasa', 'Bethany', 'Catherina', 'Sophia', 'Francesca', 'Darnell',
                'Gretchen', 'Gertrude', 'Geronimo', 'George', 'Gargantan', 'Hollie',
                'Lisa', 'Rose', 'Jennie', 'Jisoo']
    app.qtypes = ['ct', 'conceptual', 'freeresponse']
    
    for i in range(app.numStudents):
        # students
        name = app.names[random.randrange(0,len(app.names)-1)]
        qtype = app.qtypes[random.randrange(0,len(app.qtypes)-1)]
        app.students.append(Student(name, qtype))
        studLeft = app.width/3-20 if i//3 == 0 else 2*app.width/3-20
        studTop = (app.height/2)-220+(150*(i%3))
        app.students[i].setPosition(studLeft, studTop)

        # tables
        app.tables.append(Table())
        tableLeft = app.width/3-50 if i//3 == 0 else 2*app.width/3-50
        tableTop = (app.height/2)-150+(150*(i%3))
        app.tables[i].setPosition(tableLeft, tableTop)
    
    randomQueueIndices = random.sample(range(0, 6), 6)
    app.queue = []
    for i in randomQueueIndices:
        app.queue.append([app.students[i].name, i, False])

def redrawAll(app):
    app.main_player.drawItem()

    for i in range(app.numStudents): 
        app.students[i].drawItem()
        app.tables[i].drawItem()
        drawLabel(f'{app.students[i].name}', app.tables[i].left+50, app.tables[i].top+50)
        drawLabel(f'{app.queue[i]}' ,50+i*120, 10)

    if app.message != None:
        drawLabel(app.message, app.width/2, 650)

    if app.selectedQuestion != None:
        if app.currStudent != None and checkQueue(app, *app.currStudent):
            app.selectedQuestion.drawCodeTracing(app)
        elif app.currStudent == None: 
            app.selectedQuestion.drawCodeTracing(app)

def onKeyPress(app, key):
    if app.selectedQuestion != None:
        if key == 'enter':
            app.selectedQuestion.modifyAnswer('enter')
            if app.selectedQuestion.solved == True:
                app.score += 1
                app.queue[app.queuePosition][2] = True
                app.queuePosition = (app.queuePosition + 1)
                if app.queuePosition == app.numStudents:
                    studentsAndTablesAndQueue(app)
                    app.queuePosition = 0
                app.selectedQuestion = None
        elif key == 'backspace':
            app.selectedQuestion.modifyAnswer('delete')
        else:
            app.selectedQuestion.modifyAnswer('add', key)

def onKeyHold(app, keys):
    if not app.main_player.disableIntersection():
        app.main_player.move(keys)
    else:
        left, top, isLeft, isRight, isTop, isBottom, index = app.main_player.disableIntersection()
        app.currStudent = (left, top, index)

        if checkQueue(app, *app.currStudent):
            app.message = 'Press space to help the student'
            if 'space' in keys:
                # app.students[index].chooseQuestion()
                app.selectedQuestion = CodeTracing.codetracings[0]

        else:
            app.main_player.changeIntersection(isLeft, isRight, isTop, isBottom)
            app.message = 'Go help the next student in queue'
            app.currStudent = None

def checkQueue(app, left, top, index):
    queueName = app.queue[app.queuePosition][0]
    positions = Student.studentPositions
    studentIndex = positions.index((left, top, index))
    return app.students[studentIndex].name == queueName

def main():
    runApp()
main()