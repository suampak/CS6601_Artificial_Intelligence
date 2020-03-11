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
        self.nextMoves = self.__generateAllMoves()

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

    def run(self, mode = 'mymoves', depth = 5):
        m = len(self.isVisited)
        n = len(self.isVisited[0])
        print 'Start {}x{} Isolation Game...\n'.format(m,n)
        while len(self.nextMoves):
            i, j = -1, -1
            if self.isP1:
                while not self.__selMove(i,j):
                    i, j = input('Choose next move: ')
                print 'Player chose {},{}'.format(i,j)
            else:
                if mode == 'win-lose':
                    i, j = self.__calNextMove()
                elif mode == 'random':
                    i, j = self.__calNextMoveRandom()
                elif mode == 'mymoves':
                    args = [self.isVisited, self.p1]
                    i, j = self.__calNextMoveWithEval(depth, IsolationGame.myMoves, \
                                                      args)
                print 'Opponent chose {},{}'.format(i,j)
            print self
        if self.isP1:
            print 'Opponent wins :('
        else:
            print 'Player wins :)'

    def __selMove(self, i, j):
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
            self.nextMoves = self.__generateAllMoves()
            return True
        return False

    def __calNextMove(self):
        pos = self.p1 if self.isP1 else self.p2
        prevPos = [pos[0],pos[1]]
        for nexti, nextj in self.nextMoves:
            self.isVisited[nexti][nextj] = True
            pos[0] = nexti
            pos[1] = nextj
            if IsolationGame.calNextMoveImpl(self.isVisited, self.p1, self.p2, not self.isP1):
                self.isP1 = not self.isP1
                self.nextMoves = self.__generateAllMoves()
                return nexti, nextj
            self.isVisited[nexti][nextj] = False
            pos[0] = prevPos[0]
            pos[1] = prevPos[1]

        return self.__calNextMoveRandom()

    def __calNextMoveWithEval(self, depth, eval, args):
        pos = self.p1 if self.isP1 else self.p2
        prevPos = [pos[0],pos[1]]
        minmax = float('inf')
        ret = [-1,-1]
        for nexti, nextj in self.nextMoves:
            self.isVisited[nexti][nextj] = True
            pos[0] = nexti
            pos[1] = nextj
            val = IsolationGame.calNextMoveWithEvalImpl(self.isVisited, \
                                                        self.p1, self.p2, \
                                                        not self.isP1, \
                                                        depth-1, eval, args)
            if val < minmax:
                minmax = val
                ret = [nexti, nextj]
            self.isVisited[nexti][nextj] = False
            pos[0] = prevPos[0]
            pos[1] = prevPos[1]

        self.isP1 = not self.isP1
        self.isVisited[ret[0]][ret[1]] = True
        pos[0] = ret[0]
        pos[1] = ret[1]
        self.nextMoves = self.__generateAllMoves()
        return ret

    def __calNextMoveRandom(self):
        pos = self.p1 if self.isP1 else self.p2
        i,j = random.choice(self.nextMoves)
        self.isVisited[i][j] = True
        pos[0] = i
        pos[1] = j
        self.isP1 = not self.isP1
        self.nextMoves = self.__generateAllMoves()
        return i,j

    def __generateAllMoves(self):
        pos = self.p1 if self.isP1 else self.p2
        return self.generateAllMovesImpl(self.isVisited, pos)

    '''
        static method
    '''

    @staticmethod
    def calNextMoveImpl(isVisited, p1, p2, isP1):
        '''
            Return True if p1 loses
        '''
        pos = p1 if isP1 else p2
        allMoves = IsolationGame.generateAllMovesImpl(isVisited, pos)
        if len(allMoves) == 0:
            return True if isP1 else False

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

    @staticmethod
    def calNextMoveWithEvalImpl(isVisited, p1, p2, isP1, depth, eval, args):
        pos = p1 if isP1 else p2
        allMoves = IsolationGame.generateAllMovesImpl(isVisited, pos)
        if depth == 0 or len(allMoves) == 0:
            return eval(args)

        # find max if P1's turn, min if P2's turn
        maxmin = 0 if isP1 else float('inf')
        prevPos = [pos[0],pos[1]]
        for nexti, nextj in allMoves:
            isVisited[nexti][nextj] = True
            pos[0] = nexti
            pos[1] = nextj
            val = IsolationGame.calNextMoveWithEvalImpl(isVisited, p1, p2, not isP1, depth-1, eval, args)
            maxmin = max(maxmin,val) if isP1 else min(maxmin,val)
            isVisited[nexti][nextj] = False
            pos[0] = prevPos[0]
            pos[1] = prevPos[1]

        return maxmin

    @staticmethod
    def generateAllMovesImpl(isVisited, pos):
        '''
            generate all possible next moves for given position
        '''
        curri, currj = pos
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

    '''
        eval function
    '''

    @staticmethod
    def myMoves(args):
        isVisited, pos = args
        return len(IsolationGame.generateAllMovesImpl(isVisited, pos))

'''test'''
m = 5
n = 5
P1Start = True
game = IsolationGame(m,n,P1Start)
game.run()
