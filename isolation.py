import random
import copy

class IsolationGame:
    def __init__(self, m, n, isP1):
        '''
            INPUT
            m = row of board
            n = column of board
        '''
        self.isVisited = [[False for j in range(n)] for i in range(m)]
        '''
            p1 is actual player
            p2 is AI
        '''
        self.p1 = [-1, -1]
        self.p2 = [-1, -1]
        self.isP1 = isP1
        self.nextMoves = self.generateAllMoves()

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

    def selMove(self, i, j):
        '''
            check if the provided coordinate i, j is eligible for p1 (or p2)
            and change the board status accordingly
        '''
        pos = self.p1 if self.isP1 else self.p2
        if [i,j] in self.nextMoves:
            self.isVisited[i][j] = True
            pos[0] = i
            pos[1] = j
            self.isP1 = not self.isP1
            self.nextMoves = self.generateAllMoves()
            return True
        return False

    def calNextMove(self):
        pos = self.p1 if self.isP1 else self.p2
        prevPos = [pos[0],pos[1]]
        for nexti, nextj in self.nextMoves:
            self.isVisited[nexti][nextj] = True
            pos[0] = nexti
            pos[1] = nextj
            if IsolationGame.calNextMoveImpl(self.isVisited, self.p1, self.p2, not self.isP1):
                self.isP1 = not self.isP1
                self.nextMoves = self.generateAllMoves()
                return nexti, nextj
            self.isVisited[nexti][nextj] = False
            pos[0] = prevPos[0]
            pos[1] = prevPos[1]

        return self.calNextMoveRandom()

    def calNextMoveRandom(self):
        pos = self.p1 if self.isP1 else self.p2
        i,j = random.choice(self.nextMoves)
        self.isVisited[i][j] = True
        pos[0] = i
        pos[1] = j
        self.isP1 = not self.isP1
        self.nextMoves = self.generateAllMoves()
        return i,j

    @staticmethod
    def calNextMoveImpl(isVisited, p1, p2, isP1):
        '''
            Return True if p1 loses
        '''
        allMoves = IsolationGame.generateAllMovesImpl(isVisited, p1, p2, isP1)
        if len(allMoves) == 0:
            return True if isP1 else False

        pos = p1 if isP1 else p2
        prevPos = [pos[0],pos[1]]
        for nexti, nextj in allMoves:
            isVisited[nexti][nextj] = True
            pos[0] = nexti
            pos[1] = nextj
            isP2Win = IsolationGame.calNextMoveImpl(isVisited, p1, p2, not isP1)
            isVisited[nexti][nextj] = False
            pos[0] = prevPos[0]
            pos[1] = prevPos[1]
            if (isP1 and not isP2Win) or (not isP1 and isP2Win):
                return isP2Win

        return isP1

    def generateAllMoves(self):
        return self.generateAllMovesImpl(self.isVisited, self.p1, self.p2, self.isP1)

    @staticmethod
    def generateAllMovesImpl(isVisited, p1, p2, isP1):
        '''
            generate all possible next moves for p1 (or p2)
        '''
        curri, currj = p1 if isP1 else p2
        ret = []
        if curri == -1 and currj == -1:
            ret = []
            for i in range(len(isVisited)):
                for j in range(len(isVisited[0])):
                    if not isVisited[i][j]:
                        ret.append([i,j])
        else:
            for diffi, diffj in [[-1,-1],[-1,0],[-1,1],[0,1],[1,1],[1,0],[1,-1],[0,-1]]:
                mult = 1
                while IsolationGame.isValidMove(isVisited, curri+diffi*mult, currj+diffj*mult):
                    ret.append([curri+diffi*mult, currj+diffj*mult])
                    mult += 1
        return ret

    @staticmethod
    def isValidMove(isVisited, i, j):
        return i >= 0 and i < len(isVisited) and \
               j >= 0 and j < len(isVisited[0]) and \
               not isVisited[i][j]

'''test'''
game = IsolationGame(4,4,True)
print 'Start 4x4 Isolation Game...'
while len(game.nextMoves):
    if game.isP1:
        i, j = -1, -1
        while not game.selMove(i,j):
            i, j = input('Choose next move: ')
        print 'Player chooses {},{}'.format(i,j)
    else:
        i, j = game.calNextMove()
        print 'Opponent chooses {},{}'.format(i,j)
    print game
if game.isP1:
    print 'Opponent wins :('
else:
    print 'Player wins :)'
