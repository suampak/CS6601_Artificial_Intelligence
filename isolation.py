import random

class IsolationGame:
    def __init__(self, m, n):
        '''
            INPUT
            m = row of board
            n = column of board
        '''
        '''
            0: not visited
            1: visited
            2: marked visited (for searching)
        '''
        self.isVisited = [[0 for j in range(n)] for i in range(m)]
        '''
            p1 is actual player
            p2 is AI
        '''
        self.p1 = [-1, -1]
        self.p2 = [-1, -1]

    def __str__(self):
        '''
            print the board with current status
        '''
        ret = []
        for i in range(len(self.isVisited)):
            for j in range(len(self.isVisited[0])):
                if [i,j] == self.p1:
                    ret.append('X')
                elif [i,j] == self.p2:
                    ret.append('O')
                elif self.isVisited[i][j]:
                    ret.append('#')
                else:
                    ret.append('-')
            ret.append('\n')
        return ''.join(ret)

    def selMove(self, i, j, isP1):
        '''
            check if the provided coordinate i, j is eligible for p1 (or p2)
            and change the board status accordingly
        '''
        pos = self.p1 if isP1 else self.p2
        if (pos == [-1,-1] and self.isValidMove(i,j)) or \
           [i,j] in self.generateAllMoves(isP1):
            self.isVisited[i][j] = 1
            pos[0] = i
            pos[1] = j
            return True
        return False

    def calNextMoveImpl(self, isP1):
        pos = self.p1 if isP1 else self.p2
        i,j = random.choice(self.generateAllMoves(isP1))
        self.isVisited[i][j] = 1
        pos[0] = i
        pos[1] = j
        return i,j

    def generateAllMoves(self, isP1):
        '''
            generate all possible next moves for p1 (or p2)
        '''
        curri, currj = self.p1 if isP1 else self.p2
        ret = []
        if curri == -1 and currj == -1:
            ret = []
            for i in range(len(self.isVisited)):
                for j in range(len(self.isVisited[0])):
                    ret.append([i,j])
        else:
            for diffi, diffj in [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]:
                mult = 1
                while self.isValidMove(curri+diffi*mult, currj+diffj*mult):
                    ret.append([curri+diffi*mult, currj+diffj*mult])
                    mult += 1
        return ret

    def isValidMove(self, i, j):
        return i >= 0 and i < len(self.isVisited) and \
               j >= 0 and j < len(self.isVisited[0]) and \
               self.isVisited[i][j] == 0

'''test'''
game = IsolationGame(5,5)
isP1 = False
print 'Start 5x5 Isolation Game...'
while len(game.generateAllMoves(isP1)) > 0:
    if isP1:
        i, j = -1, -1
        while not game.selMove(i,j,isP1):
            i, j = input('Choose next move: ')
        print 'Player chooses {},{}'.format(i,j)
    else:
        i, j = game.calNextMoveImpl(isP1)
        print 'Opponent chooses {},{}'.format(i,j)
    print game
    isP1 = not isP1
if isP1:
    print 'Opponent wins :('
else:
    print 'Player wins :)'
