from cmu_cs3_graphics import *
from characters.avatar import Avatar
from characters.student import Student
from characters.ta import TA
from characters.mainplayer import Main_Player
from characters.table import Table
from codeTracing import CodeTracing
import random

def onAppStart(app):
    app.isGameOver = False
    app.doingCodeTracing = False
    restart(app)

def restart(app):
    app.displayIntro = False # change to true when implementing intro screen
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
    app.winNum = len(CodeTracing.codetracings)
    app.randomOrder = random.sample(range(0, app.winNum), app.winNum)


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
    if app.isGameOver == False:
        app.main_player.drawItem()
        isQuestionOpen = False

        if app.selectedQuestion != None:
            if app.currStudent != None and checkQueue(app, *app.currStudent):
                app.selectedQuestion.drawCodeTracing(app)
                isQuestionOpen = True
            elif app.currStudent == None: 
                app.selectedQuestion.drawCodeTracing(app)
                isQuestionOpen = True

        if isQuestionOpen == False:
            drawRect(0,0,app.width, 40, fill='lightgray')
            for i in range(app.numStudents): 
                app.students[i].drawItem()
                app.tables[i].drawItem()
                drawLabel(f'{app.students[i].name}', app.tables[i].left+50, app.tables[i].top+50)
                drawLabel(f'Queue' ,50, 20, size=20)
                fill='red' if app.queue[i][2] == False else 'green'
                drawRect(-10+(app.width/(app.numStudents+1))*(i+1),0, (app.width/(app.numStudents+1))-10,40, fill=fill)
                drawLabel(f'{app.queue[i][0]}' ,50+(app.width/(app.numStudents+1))*(i+1), 20, size=15)
            if app.message != None:
                drawLabel(app.message, app.width/2, 650)

def onKeyPress(app, key):
    if not app.isGameOver:
        if app.selectedQuestion != None:
            if key == 'enter':
                app.selectedQuestion.modifyAnswer('enter')
            elif key == 'backspace':
                app.selectedQuestion.modifyAnswer('delete')
            else:
                app.selectedQuestion.modifyAnswer('add', key)

    if app.isGameOver == True and key == 'r':
        restart(app)

def onKeyHold(app, keys):
    if not app.isGameOver:
        if not app.main_player.disableIntersection():
            app.main_player.move(keys)
        else:
            left, top, isLeft, isRight, isTop, isBottom, index = app.main_player.disableIntersection()
            app.currStudent = (left, top, index)

            if checkQueue(app, *app.currStudent):
                app.message = 'Press space to help the student'
                if 'space' in keys:
                    if app.selectedQuestion == None or app.selectedQuestion.solved != True:
                        if app.winNum != app.score:
                            randomNum = app.randomOrder[app.score]
                            app.selectedQuestion = CodeTracing.codetracings[randomNum]
                        else:
                            app.isGameOver = True
                    app.doingCodeTracing = True

            else:
                app.main_player.changeIntersection(isLeft, isRight, isTop, isBottom)
                app.message = 'Go help the next student in queue'
                app.currStudent = None

def onMousePress(app, mouseX, mouseY):
    if app.selectedQuestion != None and (860 <= mouseX <= 1010 and 570 <= mouseY <= 610):
            app.selectedQuestion.checkAnswer()
            if app.selectedQuestion.solved == True:
                    app.score += 1
                    app.queue[app.queuePosition][2] = True
                    app.queuePosition = (app.queuePosition + 1)
                    if app.queuePosition == app.numStudents:
                        studentsAndTablesAndQueue(app)
                        app.queuePosition = 0
                    app.selectedQuestion = None

def checkQueue(app, left, top, index):
    queueName = app.queue[app.queuePosition][0]
    positions = Student.studentPositions
    studentIndex = positions.index((left, top, index))
    return app.students[studentIndex].name == queueName

def main():
    runApp()
main()