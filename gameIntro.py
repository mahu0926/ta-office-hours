# runAppWithScreensDemo2.py
# This version works in both the sandbox and on the desktop.
# It does so by including the definition of runAppWithScreens, which
# is not yet in the desktop's cmu_graphics file.  It also has a modified
# import that works both in the sandbox and on the desktop.

# improved import:
from cmu_cs3_graphics import *
# from codeTracing import codeTracing
# from freeResponses import freeResponse

##################################################################
# runAppWithScreens() and setActiveScreen(screen)
##################################################################

def runAppWithScreens(initialScreen, *args, **kwargs):
    appFnNames = ['onAppStart',
                  'onKeyPress', 'onKeyHold', 'onKeyRelease',
                  'onMousePress', 'onMouseDrag', 'onMouseRelease',
                  'onMouseMove', 'onStep', 'redrawAll']
             
    def checkForAppFns():
        globalVars = globals()
        for appFnName in appFnNames:
            if appFnName in globalVars:
                raise Exception(f'Do not define {appFnName} when using screens')
   
    def getScreenFnNames(appFnName):
        globalVars = globals()
        screenFnNames = [ ]
        for globalVarName in globalVars:
            screenAppSuffix = f'_{appFnName}'
            if globalVarName.endswith(screenAppSuffix):
                screenFnNames.append(globalVarName)
        return screenFnNames
   
    def wrapScreenFns():
        globalVars = globals()
        for appFnName in appFnNames:
            screenFnNames = getScreenFnNames(appFnName)
            if (screenFnNames != [ ]) or (appFnName == 'onAppStart'):
                globalVars[appFnName] = makeAppFnWrapper(appFnName)
   
    def makeAppFnWrapper(appFnName):
        if appFnName == 'onAppStart':
            def onAppStartWrapper(app):
                globalVars = globals()
                for screenFnName in getScreenFnNames('onScreenStart'):
                    screenFn = globalVars[screenFnName]
                    screenFn(app)
            return onAppStartWrapper
        else:
            def appFnWrapper(*args):
                globalVars = globals()
                screen = globalVars['_activeScreen']
                wrappedFnName = ('onScreenStart'
                                 if appFnName == 'onAppStart' else appFnName)
                screenFnName = f'{screen}_{wrappedFnName}'
                if screenFnName in globalVars:
                    screenFn = globalVars[screenFnName]
                    return screenFn(*args)
            return appFnWrapper

    def go():
        checkForAppFns()
        wrapScreenFns()
        setActiveScreen(initialScreen)
        runApp(*args, **kwargs)
   
    go()

def setActiveScreen(screen):
    globalVars = globals()
    if (screen in [None, '']) or (not isinstance(screen, str)):
        raise Exception(f'{repr(screen)} is not a valid screen')
    redrawAllFnName = f'{screen}_redrawAll'
    if redrawAllFnName not in globalVars:
        raise Exception(f'Screen {screen} requires {redrawAllFnName}()')
    globalVars['_activeScreen'] = screen

##################################################################
# end of runAppWithScreens() and setActiveScreen(screen)
##################################################################

##################################
# Screen1
##################################

def splash_onScreenStart(app):
    app.color = 'gold'
    app.startButton = 400

def splash_onMousePress(app, mouseX, mouseY):
    if (app.width/2 - 125 <= mouseX <= app.width/2 + 125) and (550 <= mouseY <= 610):
        setActiveScreen('intro')

def splash_redrawAll(app):
    drawRect(0, 0, app.width, app.height, fill='blue')
    drawString(app, '15-112 OFFICE HOURS', 50, 200, 15, 'white')
    drawString(app, 'Sign in to begin!', app.width/2-275, 350, 10, 'white')
    drawRect(app.width/2 - 125, 550, 250, 60, fill='white', border='gray')
    drawString(app, 'Sign in as a TA', app.width/2-110, 590, 4, 'dimGray')

##################################
# Screen2
##################################

def intro_onScreenStart(app):
    app.speaker = 'Lauren'
    app.speechCount = 0
    app.instructions = ["Congratulations on becoming a 15-112 TA, and welcome \
to your\nfirst office hours! I know it can be kind of hectic, but you'll\nbe \
okay. Here's some tips and tricks to help you:", 'Use the arrow keys to move.\
A red exclamation mark will appear\nif you get close enough to \
a character. Press the spacebar to\ninteract with them.', 
"Your main goal is to help all of the students on the queue. \
You\ncan access the queue by pressing the list button in the top right\ncorner.\
 Click it to see a sample queue.",
"There are three tasks that you will help students with. First is\ncode tracing.\
These students are stuck on a CT, so you must type\nin the correct answer. Let's see how that works.",
"Great job! Next up is the free response questions. Help these\nstudents debug! \
Select the line that contains the error.",
"Awesome, you did it!!! Last up is the conceptual questions. Select\nthe bubble of the correct answer for the question.",
"Nice! When the queue is empty, you're free to go. Let me know if\nyou have any other \
questions. Off you go!"]
    app.showQueue = False
    # character attributes
    app.pixelSize = 5 
    app.avatarWidth = 40
    app.avatarHeight = 100
    app.playerTop = 250
    app.playerLeft = 100
    # text attributes
    app.cellBorderWidth = 1
    app.cellWidth = 7
    app.cellHeight = 7
    app.lettersToPixels = dict()
    app.lettersToPixelsAnnoying = dict()
    makePixelDict(app)
    loadAvatars(app)
    # tasks!
    loadCodeTracings(app)
    loadFreeResponses(app)
    loadConceptual(app)
    app.codeTracing = False
    app.ct = codeTracing(*app.codeTracings[0])
    app.ctWin = None
    app.freeResponse = False
    app.frq = freeResponse(*app.freeResponses[0])
    app.frqWin = None
    app.concept = False
    app.problem = conceptual(*app.conceptual[0])

def intro_onKeyPress(app, key):
    if app.codeTracing:
        if key == 'enter':
            app.ct.modifyAnswer('enter')
        elif key == 'backspace':
            app.ct.modifyAnswer('delete')
        else:
            app.ct.modifyAnswer('add', key)
    elif key == 'n': 
        app.speechCount += 1
        if app.speechCount == 4:
            app.codeTracing = True
        elif app.speechCount == 5:
            app.freeResponse = True
        elif app.speechCount == 6:
            app.concept = True
        else:
            app.concept = False
        if app.speechCount == len(app.instructions):
            app.speaker = 'You'
        elif app.speechCount > len(app.instructions):
            setActiveScreen('main')

def intro_onKeyHold(app, keys):
    if app.speechCount >= 1:
        if 'up' in keys:
            app.playerTop -= 5
        if 'down' in keys:
            app.playerTop += 5
        if 'left' in keys:
            app.playerLeft -= 5
        if 'right' in keys:
            app.playerLeft += 5

def intro_onMousePress(app, mouseX, mouseY):
    if app.codeTracing:
        if 860 <= mouseX <= 1010 and 570 <= mouseY <= 610:
            app.ctWin = app.ct.checkAnswer()
            if app.ctWin:
                app.codeTracing = False
            else:
                app.ct.resetAnswer()
    elif app.freeResponse:
        app.frq.setLine(mouseX, mouseY)
        if app.frq.check():
            app.freeResponse = False
        else:
            app.frqWin = False
    elif app.concept:
        app.problem.setAnswer(mouseX, mouseY)
        if app.problem.check(mouseX, mouseY):
            app.concept = False
            print(app.codeTracing, app.freeResponse, app.concept)
    if not (app.codeTracing or app.freeResponse or app.concept) and app.speechCount >= 2:
        if distance(mouseX, mouseY, app.width-30, 30) < 20:
            app.showQueue = not app.showQueue

def intro_onMouseMove(app, mouseX, mouseY):
    app.frq.setLine(mouseX, mouseY)

def intro_redrawAll(app):
    # background
    drawImage("https://i.ibb.co/DRbhNJn/pixil-frame-0-3.png", 0, 0, width=1200)
    if not (app.codeTracing or app.freeResponse or app.concept):
        # characters
        drawItem(app, app.playerAvatar, app.playerAvatarColors, app.playerLeft, app.playerTop)
        drawItem(app, app.denizAvatar, app.denizAvatarColors, 400, 400)
        drawItem(app, app.livAvatar, app.livAvatarColors, 600, 400)

        drawImage('https://i.ibb.co/Vx5NBFH/pixil-frame-0-2.png', 750, 200, width=300, height=450)
        ### instructions
        drawImage("https://i.ibb.co/W3C0swx/pixil-frame-0-8.png", 125, 570)
        drawInstructions(app)
        drawString(app, 'Press n to continue', 860, 750, 2.3, 'darkGray')
        ### Queue
        drawCircle(app.width-30, 30, 20, fill='white', border='black')
        if app.showQueue:
            drawQueue(app)
            drawLine(app.width-35, 22, app.width-25, 38, lineWidth=2)
            drawLine(app.width-35, 38, app.width-25, 22, lineWidth=2)
        else:
            for x in range(3):
                y = 22 + 8*x
                drawLine(app.width-40, y, app.width-20, y)
    else:
        drawImage("https://i.ibb.co/z8n2Md6/pixil-frame-0-7.png", 200, 25, height=750)
        if app.codeTracing:
            app.ct.drawCodeTracing()
            if app.ctWin == False:
                drawLabel('That is not correct! Note: all characters must be exact', 
                           580, 600, fill='red', font='monotone', size=16)
        elif app.freeResponse:
            app.frq.drawFreeResponse()
            if app.frqWin == False:
                drawLabel('That is not correct! Try again', 
                           600, 700, fill='red', font='monotone', size=16)
        elif app.conceptual:
            app.problem.drawConceptual()
            if app.problem.wrong:
                drawLabel('That is not correct! Try again', 
                           600, 600, fill='red', font='monotone', size=16)

def drawInstructions(app):
    startY = 660
    if app.speaker == 'Lauren':
        instruction = app.instructions[app.speechCount]
        fill='red'
    else:
        instruction = 'Thanks.'
        fill = 'blue'
    drawString(app, app.speaker, 250-7*len(app.speaker), 610, 3.5, fill)
    for line in instruction.splitlines():
        drawString(app, line, app.width/2 - 425, startY, 3.5, 'black')
        startY += 35

def drawQueue(app):
    drawRect(app.width/2-300, app.height/2-350, 600, 700, fill='white', border='black')
    studentCenter = 350
    taskCenter = 550
    locCenter = 730
    drawString(app, 'Student', studentCenter-5*len('Student'), 100, 6, 'black')
    drawString(app, 'Task', taskCenter-5*len('Task'), 100, 6, 'black')
    drawString(app, 'Location', locCenter-5*len('Location'), 100, 6, 'black')
    queue = [('Lauren', 'CT', 'Table 1'), ('Deniz', 'FRQ', 'Table 2'), ('Liv', 'Conceptual', 'Table 4')]
    for i in range(len(queue)):
        student, task, loc = queue[i]
        row = 200 + 100*i
        drawString(app, student, studentCenter-3*len(student), row, 4, 'black')
        drawString(app, task, taskCenter-2*len(task), row, 4, 'black')
        drawString(app, loc, locCenter-2*len(loc), row, 4, 'black')

def distance(x1, y1, x2, y2):
    return ((x2-x1)**2 + (y2-y1)**2)**0.5

###### main gameplay screen ####
def main_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill='green')

def main_onKeyPress(app, key):
    setActiveScreen('intro')

######################## storage stuff ######################## 
def loadAvatars(app):
    app.playerAvatarColors = ['black', 'peachPuff', 'blue', 'lightBlue']
    app.playerAvatar = [[0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 1, 2, 2, 1, 2, 1],
                        [0, 2, 1, 2, 2, 1, 2, 1],
                        [0, 2, 2, 2, 2, 2, 2, 1],
                        [0, 0, 2, 2, 2, 2, 0, 0],
                        [0, 0, 0, 2, 2, 0, 0, 0],
                        [3, 3, 3, 3, 3, 3, 3, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 1, 0, 0, 1, 0, 0]]
    app.laurenAvatarColors = [rgb(122, 92, 85), 'peachPuff', 'crimson', 'blue', 'black']
    app.laurenAvatar = [[0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 1, 2, 2, 2, 2, 1, 1],
                        [1, 1, 1, 2, 2, 1, 1, 1],
                        [3, 3, 3, 3, 3, 3, 3, 3],
                        [3, 1, 3, 3, 3, 3, 1, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 4, 4, 4, 4, 4, 4, 0],
                        [0, 4, 4, 4, 4, 4, 4, 0],
                        [0, 0, 2, 0, 0, 2, 0, 0],
                        [0, 0, 2, 0, 0, 2, 0, 0],
                        [0, 0, 5, 0, 0, 5, 0, 0]]
    app.denizAvatarColors = [rgb(69, 51, 31), 'peachPuff', 'dodgerBlue', 'darkGray', 'black']
    app.denizAvatar =  [[0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [0, 2, 5, 2, 2, 5, 2, 0],
                        [0, 1, 2, 2, 2, 2, 1, 0],
                        [0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 0, 0, 2, 2, 0, 0, 0],
                        [3, 3, 3, 3, 3, 3, 3, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 2, 0, 0, 2, 0, 0],
                        [0, 0, 2, 0, 0, 2, 0, 0],
                        [0, 0, 5, 0, 0, 5, 0, 0]]
    app.livAvatarColors = ['burlyWood', 'peachPuff', 'lavender', 'blue', 'black']
    app.livAvatar =    [[0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [1, 2, 2, 2, 2, 2, 2, 0],
                        [1, 1, 2, 2, 2, 2, 0, 0],
                        [1, 1, 1, 2, 2, 0, 0, 0],
                        [3, 1, 1, 3, 3, 3, 3, 3],
                        [3, 1, 1, 3, 3, 3, 0, 3],
                        [3, 1, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 5, 0, 0, 5, 0, 0]]
    app.kozAvatarColors = ['peru', 'peachPuff', 'blue', 'tan', 'black']
    app.kozAvatar =    [[0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [0, 2, 5, 2, 2, 5, 2, 0],
                        [0, 2, 2, 2, 2, 2, 2, 0],
                        [0, 0, 2, 2, 2, 2, 0, 0],
                        [0, 0, 0, 2, 2, 0, 0, 0],
                        [3, 3, 3, 3, 3, 3, 3, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [3, 0, 3, 3, 3, 3, 0, 3],
                        [2, 0, 3, 3, 3, 3, 0, 2],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 4, 4, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 4, 0, 0, 4, 0, 0],
                        [0, 0, 5, 0, 0, 5, 0, 0]]

def drawItem(app, item, colors, left, top):
    rows, cols = len(item), len(item[0])
    for row in range(rows):
        for col in range(cols):
            if item[row][col] != 0:
                color = colors[item[row][col]-1]
            else:
                color = None
            pixelLeft, pixelTop = getPixelLeftTop(app, row, col, left, top)
            drawRect(pixelLeft, pixelTop, app.pixelSize, app.pixelSize,
                     fill=color)
 
def getPixelLeftTop(app, row, col, left, top):
    left = left + col * app.pixelSize
    top = top + row * app.pixelSize
    return left, top

def makePixelDict(app):
 lettera = [[0, 1, 1, 0, 0, 0],
             [1, 0, 1, 1, 0, 0],
             [1, 1, 1, 0, 1, 0]]
 letterb = [[1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letterc = [[1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0]]
 letterd = [[0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 lettere = [[0, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [1, 0, 0, 0],
             [0, 1, 1, 0]]
 letterf = [[0, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 0, 0]]
 letterg = [[0, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [0, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0]]
 letterh = [[1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0]]
 letteri = [[0, 0],
             [1, 0],
             [0, 0],
             [1, 0],
             [1, 0]]
 letterj = [[0, 0, 1, 0],
             [0, 0, 0, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0]]
 letterk = [[1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0]]
 letterl = [[1, 0],
             [1, 0],
             [1, 0],
             [1, 0],
             [1, 0]]
 letterm = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0, 0],
             [1, 0, 1, 0, 1, 0],
             [1, 0, 1, 0, 1, 0]]
 lettern = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [0, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0]]
 lettero = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letterp = [[1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 0, 0, 0]]
 letterq = [[0, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]]
 letterr = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 0, 0]]
 letters = [[1, 1, 0],
             [1, 0, 0],
             [0, 1, 0],
             [1, 1, 0]]
 lettert = [[0, 0, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
 letteru = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letterv = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0]]
 letterw = [[0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1, 0],
             [1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 0]]
 letterx = [[0, 0, 0, 0],
             [0, 0, 0, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0],
             [1, 0, 1, 0]]
 lettery = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0]]
 letterz = [[1, 1, 0],
             [0, 1, 0],
             [1, 0, 0],
             [1, 1, 0]]
 letterA = [[0, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0]]
 letterB = [[1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letterC = [[1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0]]
 letterD = [[1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 0, 0]]
 letterE = [[1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0]]
 letterF = [[1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 0, 0],
             [1, 0, 0, 0]]
 letterG = [[1, 1, 1, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 0, 1, 1, 0],
             [1, 0, 0, 1, 0],
             [0, 1, 1, 0, 0]]
 letterH = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0]]
 letterI = [[1, 1, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [1, 1, 1, 0]]
 letterJ = [[0, 1, 1, 1, 0],
             [0, 0, 1, 0, 0],
             [0, 0, 1, 0, 0],
             [1, 0, 1, 0, 0],
             [0, 1, 1, 0, 0]]
 letterK = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0]]
 letterL = [[1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0]]
 letterM = [[1, 0, 0, 0, 1, 0],
             [1, 1, 0, 1, 1, 0],
             [1, 0, 1, 0, 1, 0],
             [1, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 1, 0]]
 letterN = [[1, 0, 0, 1, 0],
             [1, 0, 0, 1, 0],
             [1, 1, 0, 1, 0],
             [1, 0, 1, 1, 0],
             [1, 0, 0, 1, 0]]
 letterO = [[0, 1, 1, 0, 0],
             [1, 0, 0, 1, 0],
             [1, 0, 0, 1, 0],
             [1, 0, 0, 1, 0],
             [0, 1, 1, 0, 0]]
 letterP = [[1, 1, 1, 0, 0],
             [1, 0, 0, 1, 0],
             [1, 1, 1, 0, 0],
             [1, 0, 0, 0, 0],
             [1, 0, 0, 0, 0]]
 letterQ = [[0, 1, 1, 0, 0,0],
             [1, 0, 0, 1, 0,0],
             [1, 0, 0, 1, 0,0],
             [1, 0, 0, 1, 0,0],
             [0, 1, 1, 0, 1, 0]]
 letterR = [[1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0]]
 letterS = [[1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0],
             [0, 0, 1, 0],
             [1, 1, 1, 0]]
 letterT = [[1, 1, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
 letterU = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letterV = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0]]
 letterW = [[1, 0, 0, 0, 1, 0],
             [1, 0, 0, 0, 1, 0],
             [1, 0, 1, 0, 1, 0],
             [1, 0, 1, 0, 1, 0],
             [0, 1, 0, 1, 0, 0]]
 letterX = [[1, 0, 0, 1, 0],
             [1, 0, 0, 1, 0],
             [0, 1, 1, 0, 0],
             [1, 0, 0, 1, 0],
             [1, 0, 0, 1, 0]]
 letterY = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
 letterZ = [[1, 1, 1, 1, 0],
             [0, 0, 0, 1, 0],
             [0, 1, 1, 0, 0],
             [1, 1, 0, 0, 0],
             [1, 1, 1, 1, 0]]
 letter1 = [[0, 1, 0, 0],
             [1, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0],
             [0, 1, 0, 0]]
 letter2 = [[0, 1, 0, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0],
             [1, 0, 0, 0],
             [1, 1, 1, 0]]
 letter3 = [[1, 1, 0, 0],
             [0, 0, 1, 0],
             [0, 1, 0, 0],
             [0, 0, 1, 0],
             [1, 1, 0, 0]]
 letter4 = [[1, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]]
 letter5 = [[1, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [0, 0, 1, 0],
             [1, 1, 1, 0]]
 letter6 = [[0, 1, 1, 0],
             [1, 0, 0, 0],
             [1, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letter7 = [[1, 1, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]]
 letter8 = [[1, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0]]
 letter9 = [[0, 1, 1, 0],
             [1, 0, 1, 0],
             [1, 1, 1, 0],
             [0, 0, 1, 0],
             [0, 0, 1, 0]]
 letter0 = [[0, 1, 0, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 0, 0]]
 letterPeriod = [[0, 1, 0, 0]]
 letterExcl = [[0, 1, 0],
             [0, 1,  0],
             [0, 1, 0],
             [0, 0,  0],
             [0, 1,  0]]
 letterQues = [[1, 1, 1, 0],
             [1, 0, 1, 0],
             [0, 1, 1, 0],
             [0, 0, 0, 0],
             [0, 1, 0, 0]]
 letterDash = [[0, 0, 0],
             [0, 0, 0],
             [1, 1, 0],
             [0, 0, 0],
             [0, 0, 0]]
 letterLeftParen = [[0, 1, 0],
             [1, 0, 0],
             [1, 0, 0],
             [1, 0, 0],
             [0, 1, 0]]
 letterRightParen = [[0, 1, 0],
             [0, 0, 1],
             [0, 0, 1],
             [0, 0, 1],
             [0, 1, 0]]
 letterApos = [[0, 1, 0],
             [0, 1, 0],
             [0, 0, 0],
             [0, 0, 0],
             [0, 0, 0]]
 letterColon = [[0, 0, 0],
             [0, 0, 0],
             [0, 1, 0],
             [0, 0, 0],
             [0, 1, 0]]
 letterComma = [[0, 0, 0],
             [0, 0, 0],
             [0, 0, 0],
             [0, 1, 0],
             [0, 1, 0]]
 app.lettersToPixels['a'] = lettera
 app.lettersToPixels['b'] = letterb
 app.lettersToPixels['c'] = letterc
 app.lettersToPixels['d'] = letterd
 app.lettersToPixels['e'] = lettere
 app.lettersToPixels['f'] = letterf
 app.lettersToPixels['h'] = letterh
 app.lettersToPixels['i'] = letteri
 app.lettersToPixels['k'] = letterk
 app.lettersToPixels['l'] = letterl
 app.lettersToPixels['m'] = letterm
 app.lettersToPixels['n'] = lettern
 app.lettersToPixels['o'] = lettero
 app.lettersToPixels['r'] = letterr
 app.lettersToPixels['s'] = letters
 app.lettersToPixels['t'] = lettert
 app.lettersToPixels['u'] = letteru
 app.lettersToPixels['v'] = letterv
 app.lettersToPixels['w'] = letterw
 app.lettersToPixels['x'] = letterx
 app.lettersToPixels['z'] = letterz
 
 app.lettersToPixelsAnnoying['j'] = letterj
 app.lettersToPixelsAnnoying['g'] = letterg
 app.lettersToPixelsAnnoying['p'] = letterp
 app.lettersToPixelsAnnoying['q'] = letterq
 app.lettersToPixelsAnnoying['y'] = lettery
 
 app.lettersToPixels['A'] = letterA
 app.lettersToPixels['B'] = letterB
 app.lettersToPixels['C'] = letterC
 app.lettersToPixels['D'] = letterD
 app.lettersToPixels['E'] = letterE
 app.lettersToPixels['F'] = letterF
 app.lettersToPixels['G'] = letterG
 app.lettersToPixels['H'] = letterH
 app.lettersToPixels['I'] = letterI
 app.lettersToPixels['J'] = letterJ
 app.lettersToPixels['K'] = letterK
 app.lettersToPixels['L'] = letterL
 app.lettersToPixels['M'] = letterM
 app.lettersToPixels['N'] = letterN
 app.lettersToPixels['O'] = letterO
 app.lettersToPixels['P'] = letterP
 app.lettersToPixels['Q'] = letterQ
 app.lettersToPixels['R'] = letterR
 app.lettersToPixels['S'] = letterS
 app.lettersToPixels['T'] = letterT
 app.lettersToPixels['U'] = letterU
 app.lettersToPixels['V'] = letterV
 app.lettersToPixels['W'] = letterW
 app.lettersToPixels['X'] = letterX
 app.lettersToPixels['Y'] = letterY
 app.lettersToPixels['Z'] = letterZ
 
 app.lettersToPixels['1'] = letter1
 app.lettersToPixels['2'] = letter2
 app.lettersToPixels['3'] = letter3
 app.lettersToPixels['4'] = letter4
 app.lettersToPixels['5'] = letter5
 app.lettersToPixels['6'] = letter6
 app.lettersToPixels['7'] = letter7
 app.lettersToPixels['8'] = letter8
 app.lettersToPixels['9'] = letter9
 app.lettersToPixels['0'] = letter0
 app.lettersToPixels['.'] = letterPeriod
 app.lettersToPixels[','] = letterComma
 app.lettersToPixels['!'] = letterExcl
 app.lettersToPixels['?'] = letterQues
 app.lettersToPixels['-'] = letterDash
 app.lettersToPixels['('] = letterLeftParen
 app.lettersToPixels[')'] = letterRightParen
 app.lettersToPixels["'"] = letterApos
 app.lettersToPixels[':'] = letterColon

def drawString(app, string, startingX, startingY, size, color):
 leftX = startingX
 bottomY = startingY
 for char in string:
   if not char.isspace():
     letter = getLetter(app, char)
     if char in app.lettersToPixels:
       drawLetter(app, letter, leftX, bottomY-len(letter)*size, size, color)
       leftX += len(letter[0]) * size
     else:
       drawLetter(app, letter, leftX, bottomY-3*size, size, color)
       leftX += len(letter[0]) * size
   else:
     letter = [[0] * 3]
     drawLetter(app, letter, leftX, bottomY-len(letter)*size, size, color)
     leftX += len(letter[0]) * size
 
def getLetter(app, char):
 if app.lettersToPixels.get(char) != None:
   return app.lettersToPixels.get(char)
 else:
   return app.lettersToPixelsAnnoying.get(char)
 
def drawLetter(app, letter, startingX, startingY, size, color):
 for row in range(len(letter)):
   for col in range(len(letter[0])):
     if letter[row][col] == 1:
       drawCell(app, row, col, color, startingX, startingY, size)
 
def drawCell(app, row, col, color, startingX, startingY, size, pieceOpac=100):
   cellLeft, cellTop = getCellLeftTop(app, row, col, startingX, startingY, size)
   cellWidth, cellHeight = getCellSize(app)
   drawRect(cellLeft, cellTop, size, size,
            fill=color, border=color,
            borderWidth=app.cellBorderWidth, opacity = pieceOpac)
 
def getCellLeftTop(app, row, col, startingX, startingY, size):
   cellWidth, cellHeight = getCellSize(app)
   cellLeft = startingX + col * size
   cellTop = startingY + row * size
   return (cellLeft, cellTop)
 
def getCellSize(app):
   cellWidth = app.cellWidth
   cellHeight = app.cellHeight
   return (cellWidth, cellHeight)

##################################
# main
##################################

############# class stuff because i couldn't figure out the imports ####
class codeTracing():
    def __init__(self, lines, answer):
        self.lines = lines
        self.answer = [['']]
        self.realAnswer = answer

    def drawCodeTracing(self):
        for line in range(len(self.lines)):
            drawLabel(self.lines[line], 250, 60 + (550)//len(self.lines) * line, font = 'monospace',
                      align = 'left', size = 16)
        drawRect(260, 610, 750, 100, fill = None, border = 'black')
        if self.answer != [[]]:
            for string in range(len(self.answer)):
                if self.answer[string] != []:
                    drawLabel(self.answer[string][0], 270, 630 + 20 * string, size = 16, align = 'left', font = 'monospace')
        drawRect(860, 570, 150, 40, fill='lightGreen', border='black')
        drawLabel('Submit', 890, 585, align='left-top', font='monospace', size=20)

    #modification entries are enter, add, delete as string
    def modifyAnswer(self, modification, addedChar = ''):
        if modification == 'enter':
            self.answer.append([''])
        elif modification == 'add':
            self.answer[-1][-1] += (addedChar)
        else:
            if self.answer != [['']]:
                if self.answer[-1][-1] == '':
                    self.answer.pop()
                    if len(self.answer) == 0:
                        self.answer = [['']]
                else:
                    self.answer[-1][-1] = self.answer[-1][-1][:-1]

    def checkAnswer(self):
        return self.answer == self.realAnswer
    def resetAnswer(self):
        self.answer = [['']]

def loadCodeTracings(app):
    app.codeTracings = []
    c1 = ["from cmu_cs3_utils import rounded", 
       "",
       "def f(x):",
       "    print(x+5)",
       "    return x + 2",
       "",
       "def g(x):",
       "    return rounded(x) == rounded(x + 0.5)",
       "",
       "print(f(4))",
       "print(g(2.4))",
       "print(g(2.9))"]
    c1Ans = [['9'],['6'],['False'],['True']]

    c2 = ["def f(x):",
          "    if (abs(x) <= 10):",
          "        x-=10",
          "    if (abs(x)) <= 10:",
          "        return 100*x",
          "    else:",
          "        x -= 10",
          "    return x if x > 0 else x/10"]
    c2Ans = [['-200'],['2'],['-3.0']]

    c3 = ["def ct(m, n):",
          "    for i in range(m, m + n, 3):",
          "        if (i % 10 == 3):",
          "            continue",
          "        print(i)",
          "    if (i > 61):",
          "        break",
          "ct(50, 18)"]
    c3Ans = [['50'],['56'],['59'], ['62']]

    c4 = ["def ct(c, d):",
          "    t = ''",
          "    while (c < 'L'):",
          "        c  = chr(ord(c) + d)",
          "        d += 1",
          "        t += c",
          "    return t",
          "print(ct('D', 2))"]
    c4Ans = [['FIM']]

    c5 = ["import math",
          "from cmu_cs3_utils import rounded",
          "n = 435 / 10",
          "m = math.ceil(n)",
          "print(m)",
          "q = 10 * m + 9",
          "print(q)",
          "q -= math.floor(n) % 10",
          "print(q)"]
    c5Ans = [["44"], ["449"], ["446"]]

    app.codeTracings.append((c1, c1Ans))
    app.codeTracings.append((c2, c2Ans))
    app.codeTracings.append((c3, c3Ans))
    app.codeTracings.append((c4, c4Ans))
    app.codeTracings.append((c5, c5Ans))

class freeResponse():
    def __init__(self, L, incorrectLine):
        self.lines = L
        self.incorrectLine = incorrectLine
        self.line = None

    def drawFreeResponse(self):
        for line in range(len(self.lines)):
            drawLabel(self.lines[line], 350, 60 + (550)//len(self.lines) * line + (550)//len(self.lines)/2, font = 'monospace',
                      align = 'left', size = 16)
        if self.line != None:
            y = 60 + ((550)//len(self.lines) * self.line)
            x = 350
            drawRect(x, y, 750, (550)//len(self.lines), fill = 'green', opacity = 30)
    
    def setLine(self, mouseX, mouseY):
        if mouseX < 350:
            self.line = None
        else:
            for line in range(len(self.lines)):
                y = 60 + (550)//len(self.lines) * line 
                y1 = 60 + (550)//len(self.lines) * (line + 1) 
                if y <= mouseY <= y1:
                    self.line = line
                    print(self.line)
    
    def check(self):
        return self.line == self.incorrectLine
        
class freeResponse():
    def __init__(self, L, incorrectLine):
        self.lines = L
        self.incorrectLine = incorrectLine
        self.line = None

    def drawFreeResponse(self):
        for line in range(len(self.lines)):
            drawLabel(self.lines[line], 350, 60 + (550)//len(self.lines) * line + (550)//len(self.lines)/2, font = 'monospace',
                      align = 'left', size = 16)
        if self.line != None:
            y = 60 + ((550)//len(self.lines) * self.line)
            x = 250
            drawRect(x, y, 750, (550)//len(self.lines), fill = 'green', opacity = 30)
    
    def setLine(self, mouseX, mouseY):
        if mouseX < 350:
            self.line = None
        else:
            for line in range(len(self.lines)):
                y = 60 + (550)//len(self.lines) * line 
                y1 = 60 + (550)//len(self.lines) * (line + 1) 
                if y <= mouseY <= y1:
                    self.line = line
                    print(self.line)
    
    def check(self):
        return self.line == self.incorrectLine

def loadFreeResponses(app):
    app.freeResponses = []
    f1 = ["def nthPerfectNumber(n):",
    "    numTest = 0",
    "    numPerfectNum = 0",
    "    while (numPerfectNum < n):",
        "        numTest += 1",
        "        if (isPerfectNumber(numTest)):",
            "            numPerfectNum += 1",
    "    return numTest"]
    f1Ans = 3
    app.freeResponses.append((f1, f1Ans))

class conceptual():
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.wrong = None
        self.selectedAnswer = None
    
    def drawConceptual(self):
        drawLabel(self.question[0], 350, 70, size = 16, bold = True, font = 'monospace', align = 'left')
        for line in range(1,len(self.question)):
            y = 30 * (line) + 70
            drawLabel(self.question[line], 350, y, size = 16, font = 'monospace', align = 'left')
        for choice in range(len(self.choices)):
            y = 30 * len(self.question) + 70 + choice * 30
            if choice == self.selectedAnswer:
                color = 'black'
            else:
                color = None
            drawCircle(350, y, 10, fill = color, border = 'black')
            drawLabel(self.choices[choice], 385, y, size = 16, font = 'monospace', align = 'left')
        drawRect(600, 700, 600, 100, align = 'center', fill = None, border = 'black')
        drawLabel("SUBMIT", 600, 700, bold = True, size = 40)

    def setAnswer(self, mouseX, mouseY):
        for choice in range(len(self.choices)):
            x = 350
            y = 30 * len(self.question) + 70 + choice * 30
            if conceptual.distance(x, y, mouseX, mouseY) <= 10:
                self.selectedAnswer = choice
                break

    def check(self, mouseX, mouseY):
        if 300 <= mouseX <= 900 and 650 <= mouseY <= 750:
            if not self.selectedAnswer == self.answer:
                self.wrong = True
            return self.selectedAnswer == self.answer
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x0-x1)**2 + (y0-y1)**2) ** 0.5


def loadConceptual(app):
    app.conceptual = []
    ques1 = ['What is the efficiency of: ', 
            'def min(L):',
             '    smallest = None',
            '    for v in L:',
        '        if smallest == None or v < smallest:',
            '            smallest = v',
    '    return smallest']
    choices1 = ['O(N)', 'O(N^2)', 'O(logN)', 'O(NlogN)']
    ans1 = 0
    app.conceptual.append((ques1, choices1, ans1))

def main():
    runAppWithScreens(initialScreen='splash', width=1200, height=800)

main()