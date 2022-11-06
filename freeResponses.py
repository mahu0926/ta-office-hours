#To initialize do freeResponse(*app.freeResponses[num])

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
        

def loadFreeResponses(app):
    app.freeResponses()
    f1 = ["def nthPerfectNumber(n):",
    "    numTest = 0",
    "    numPerfectNum = 0",
    "    while (numPerfectNum < n):",
        "        numTest += 1",
        "        if (isPerfectNumber(numTest)):",
            "            numPerfectNum += 1",
    "    return numTest"]
    f1Ans = 3

def onMouseMove(app, mouseX, mouseY):
    app.freeResponse1.setLine(mouseX, mouseY)

def onMousePress(app, mouseX, mouseY):
    app.freeResponse1.setLine(mouseX, mouseY)
    if app.freeResponse1.check():
        #do something idk
        pass

def redrawAll(app):
    drawImage("https://i.ibb.co/z8n2Md6/pixil-frame-0-7.png",300, 25, height = 
            750)