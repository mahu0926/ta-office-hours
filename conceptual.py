class conceptual():
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices
        self.answer = answer
        self.selectedAnswer = None
    
    def drawQuestion(self):
        drawLabel(self.question[0], 360, 70, size = 16, bold = True, font = 'monospace', align = 'left')
        for line in range(1,len(self.question)):
            y = 30 * (line) + 70
            drawLabel(self.question[line], 360, y, size = 16, font = 'monospace', align = 'left')
        for choice in range(len(self.choices)):
            y = 30 * len(self.question) + 70 + choice * 30
            if choice == self.selectedAnswer:
                color = 'black'
            else:
                color = None
            drawCircle(370, y, 10, fill = color, border = 'black')
            drawLabel(self.choices[choice], 385, y, size = 16, font = 'monospace', align = 'left')
        drawRect(750, 700, 600, 100, align = 'center', fill = None, border = 'black')
        drawLabel("SUBMIT", 750, 700, bold = True, size = 40)

    def setAnswer(self, mouseX, mouseY):
        for choice in range(len(self.choices)):
            x = 370
            y = 30 * len(self.question) + 70 + choice * 30
            if conceptual.distance(x, y, mouseX, mouseY) <= 10:
                self.selectedAnswer = choice
                break

    def check(self, mouseX, mouseY):
        if 450 <= mouseX <= 1050 and 650 <= mouseY <= 750:
            print(self.selectedAnswer == self.answer)
            return self.selectedAnswer == self.answer
    
    @staticmethod
    def distance(x0, y0, x1, y1):
        return ((x0-x1)**2 + (y0-y1)**2) ** 0.5


def loadConceptual(app):
    app.concenptual = []
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