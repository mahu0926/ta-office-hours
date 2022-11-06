from cmu_cs3_graphics import *
from .avatar import Avatar
from .student import Student

class Main_Player(Avatar):

    def __init__(self, name, left, top):
        super().__init__(name)
        self.avatar = [ [0, 0, 1, 1, 1, 1, 0, 0],
                        [0, 1, 1, 1, 1, 1, 1, 0],
                        [1, 2, 2, 2, 2, 2, 2, 1],
                        [1, 2, 5, 2, 2, 5, 2, 1],
                        [0, 2, 5, 2, 2, 5, 2, 1],
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
                        [0, 0, 5, 0, 0, 5, 0, 0]]
        self.colors = ['black', 'peachPuff', 'blue', 'lightBlue', 'black']
        self.label = 'Main Player'
        self.left, self.top = left-self.width/2, top-self.height/2

    def disableIntersection(self):
        positions = Student.studentPositions
        for (left, top, index) in positions:
            width = self.width
            height = self.height
            right, bottom  = (left+width, top+height)

            mpleft = self.left
            mptop = self.top
            mpright = mpleft + width
            mpbottom = mptop + height

            isLeft, isRight, isTop, isBottom = (False, False, False, False)

            if mpright >= left and right >= mpright: # right
                isRight = True
            elif mpleft <= right and left <= mpleft: # left
                isLeft = True
            if mptop <= bottom and mptop >= top: # top
                isTop = True
            elif mpbottom >= top and mpbottom <= bottom: # bottom
                isBottom = True    
            if (isRight or isLeft) and (isTop or isBottom):
                return (left, top, isLeft, isRight, isTop, isBottom, index)
        return False
            
    def changeIntersection(self, isLeft, isRight, isTop, isBottom):
        if (isLeft or isRight) and (isTop or isBottom):
            if isLeft:
                self.left += 10
            elif isRight:
                self.left -= 10
            if isTop:
                self.top -= 10
            elif isBottom:
                self.top += 10
        #     return True
        # return False



        


