#To load do codeTracing(*app.codeTracings[number])
#Have to have button to check

class codeTracing():
    def __init__(self, lines, answer):
        self.lines = lines
        self.answer = [['']]
        self.realAnswer = answer

    def drawCodeTracing(self):
        for line in range(len(self.lines)):
            drawLabel(self.lines[line], 350, 60 + (550)//len(self.lines) * line, font = 'monospace',
                      align = 'left', size = 16)
        drawRect(360, 610, 750, 100, fill = None, border = 'black')
        if self.answer != [[]]:
            for string in range(len(self.answer)):
                if self.answer[string] != []:
                    drawLabel(self.answer[string][0], 370, 630 + 20 * string, size = 16, align = 'left', font = 'monospace')
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

def onKeyPress(app, key):
    if key == 'enter':
        app.codeTracing1.modifyAnswer('enter')
    elif key == 'backspace':
        app.codeTracing1.modifyAnswer('delete')
    else:
        app.codeTracing1.modifyAnswer('add', key)

def redrawAll(app):
    drawImage("https://i.ibb.co/z8n2Md6/pixil-frame-0-7.png",300, 25, height = 
            750)
