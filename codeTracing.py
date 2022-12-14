#To load do codeTracing(*app.codeTracings[number])
#Have to have button to check
from cmu_cs3_graphics import *

class CodeTracing():
    codetracings = []
    index = 0

    def __init__(self, lines, answer):
        self.lines = lines
        self.answer = [['']]
        self.solved = False
        self.realAnswer = answer
        self.index = CodeTracing.index
        self.ctWin = None
        CodeTracing.codetracings.append(self)
        CodeTracing.index += 1

    def drawCodeTracing(self, app):
        drawImage("https://i.ibb.co/z8n2Md6/pixil-frame-0-7.png",200, 25, height = 750)
        for line in range(len(self.lines)):
            drawLabel(self.lines[line], 300, 60 + (550)//len(self.lines) * line, font = 'monospace',
                      align = 'left', size = 16)
        drawRect(250, 610, 750, 100, fill = None, border = 'black')
        if self.answer != [[]]:
            for string in range(len(self.answer)):
                if self.answer[string] != []:
                    drawLabel(self.answer[string][0], 300, 630 + 20 * string, size = 16, align = 'left', font = 'monospace')
        drawRect(860, 570, 150, 40, fill='lightGreen', border='black')
        drawLabel('Submit', 890, 585, align='left-top', font='monospace', size=20)
        if self.ctWin == False:
            drawLabel('That is not correct! Note: all characters must be exact', 
                           580, 600, fill='red', font='monotone', size=16)
    
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
        if self.answer == self.realAnswer:
            # check if the answer is correct
            self.solved = True
        else:
            self.ctWin = False
            self.resetAnswer()

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

        c6 = ["print(628%1)",
        "print(628%10)",
        "print(628%100)",
        "print(628%1000)"]
        c6Ans = [["0"], ["8"], ["28"], ["628"]]

    
        c1obj = CodeTracing(c1, c1Ans)
        c2obj = CodeTracing(c2, c2Ans)
        c3obj = CodeTracing(c3, c3Ans)
        c4obj = CodeTracing(c4, c4Ans)
        c5obj = CodeTracing(c5, c5Ans)
        c6obj = CodeTracing(c6, c6Ans)
        
