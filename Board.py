import pygame
import math
import Colors
import copy
from Value import state_value
from Node import Node

class Board:

    def __init__(self, center, len, screen, dims):
        self.center = center
        self.len = int(len)
        self.screen = screen
        self.ball_r = int(dims[0])
        self.field_r = self.ball_r - 8
        self.gap = int(dims[1])
        self.allowedRows = [[0,1],[0,1,1],[0,1,1,1],[0,1,1,1,2],[0,1,1,1,2,2],[0,1,1,2],[0,2],[0,2,2],[0,2,2,2],[0,2,2,2,1],[0,2,2,2,1,1],[0,2,2,1]]
        self.allowedKnocks = [[0,1,1,2],[0,1,1,1,2],[0,1,1,1,2,2],[0,2,2,1],[0,2,2,2,1],[0,2,2,2,1,1]]
        self.deleted = 0
        self.scorewhite = 0
        self.scoreblack = 0
        self.turn_counter = 0
        self.vertices = [(self.center[0] - self.len/2, self.center[1] - self.len*math.sqrt(3)/2),
                        (self.center[0] + self.len/2, self.center[1] - self.len*math.sqrt(3)/2),
                        (self.center[0] + self.len, self.center[1]),
                       (self.center[0] + self.len/2, self.center[1] + self.len*math.sqrt(3)/2),
                      (self.center[0] - self.len/2, self.center[1] + self.len*math.sqrt(3)/2),
                     (self.center[0] - self.len, self.center[1])]

        self.boardState = [[9,9,9,9,9,9],
                          [9,2,2,2,2,2,9],
                         [9,2,2,2,2,2,2,9],
                        [9,0,0,2,2,2,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                      [9,0,0,0,0,0,0,0,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                        [9,0,0,1,1,1,0,0,9],
                         [9,1,1,1,1,1,1,9],
                          [9,1,1,1,1,1,9],
                           [9,9,9,9,9,9]]

        self.resultState = [[9,9,9,9,9,9],
                          [9,2,2,2,2,2,9],
                         [9,2,2,2,2,2,2,9],
                        [9,0,0,2,2,2,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                      [9,0,0,0,0,0,0,0,0,0,9],
                       [9,0,0,0,0,0,0,0,0,9],
                        [9,0,0,1,1,1,0,0,9],
                         [9,1,1,1,1,1,1,9],
                          [9,1,1,1,1,1,9],
                           [9,9,9,9,9,9]]

        self.grid =     [[2,2,2,2,2],
                        [2,2,2,2,2,2],
                       [0,0,2,2,2,0,0],
                      [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                       [0,0,1,1,1,0,0],
                        [1,1,1,1,1,1],
                         [1,1,1,1,1]]

        self.coords =   [[2,2,2,2,2],
                        [2,2,2,2,2,2],
                       [0,0,2,2,2,0,0],
                      [0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0],
                      [0,0,0,0,0,0,0,0],
                       [0,0,1,1,1,0,0],
                        [1,1,1,1,1,1],
                         [1,1,1,1,1]]

    def initCoords(self):
        for i in range(9):
            if i == 0:
                curCoord = (int(self.center[0] - int(4*self.ball_r + 2*self.gap)), int(self.center[1] - 8*self.ball_r))
            if i < 5 and i != 0:
                curCoord = (curCoord[0] - int(self.ball_r + self.gap/2), curCoord[1] + 2*self.ball_r)
            if i >= 5:
                curCoord = (curCoord[0] + int(self.ball_r + self.gap/2), curCoord[1] + 2*self.ball_r)
            for j in range(len(self.coords[i])):
                self.coords[i][j] = int(curCoord[0] + (j)*(2*self.ball_r + self.gap)),int(curCoord[1])

    def initialize(self):
        self.initCoords()

    def draw(self, current_ball):
        pygame.draw.polygon(self.screen, Colors.BROWN, self.vertices)
        for i in range(9):
            for j in range(len(self.grid[i])):
                if self.boardState[i + 1][j + 1] == 0:
                    self.grid[i][j] = pygame.draw.circle(self.screen, Colors.LIGHTBROWN, self.coords[i][j], self.field_r)
                if self.boardState[i + 1][j + 1] == 1:
                    self.grid[i][j] = pygame.draw.circle(self.screen, Colors.WHITE, self.coords[i][j], self.ball_r)
                if self.boardState[i + 1][j + 1] == 2:
                    self.grid[i][j] = pygame.draw.circle(self.screen, Colors.BLACK, self.coords[i][j], self.ball_r)

        for i in range(self.scoreblack):
             pygame.draw.circle(self.screen, Colors.WHITE, (270 + i*(2*self.ball_r + self.gap), 120), self.ball_r)

        for i in range(self.scorewhite):
             pygame.draw.circle(self.screen, Colors.BLACK, (270 + i*(2*self.ball_r + self.gap), 800), self.ball_r)

        if current_ball != 0:
            pygame.draw.circle(self.screen, Colors.GREEN, self.coords[current_ball[0]][current_ball[1]], self.ball_r)


    def check_move(self, coords1, coords2):

        origx = coords1[1] + 1
        origy = coords1[0] + 1
        x1 = coords1[1] + 1
        y1 = coords1[0] + 1
        x2 = coords2[1] + 1
        y2 = coords2[0] + 1
        dir = [0, 0]
        resultState = copy.deepcopy(self.boardState)  #self.boardState copy
        player = resultState[y1][x1]
        if x1 > x2: dir[1] = -1
        if x1 < x2: dir[1] = 1
        if y1 == y2: dir[0] = 0
        if y1 > y2: dir[0] = -1
        if y1 < y2: dir[0] = 1

        if abs(y2 - y1) > 1 or abs(x2 - x1) > 1: return [False]

        rowlist = []
        coordlist = []
        deleted = 0
        rowlist.append(0)
        coordlist.append([origy, origx])
        rowlist.append(resultState[y1][x1])
        coordlist.append([y2, x2])

        while True:

            if resultState[y2][x2] == 0:
                for i in self.allowedRows:
                    if rowlist == i:
                        for j in range(len(rowlist)):
                            resultState[coordlist[j][0]][coordlist[j][1]] = rowlist[j]
                            #self.boardState[coordlist[i][0]][coordlist[i][1]] = rowlist[i]
                        return [True, resultState, [rowlist, coordlist, deleted]]
                return [False]

            if resultState[y2][x2] == 9:
                for i in self.allowedKnocks:
                    if rowlist == i:
                        deleted = rowlist.pop()
                        coordlist.pop()
                        for j in range(len(rowlist)):
                            resultState[coordlist[j][0]][coordlist[j][1]] = rowlist[j]
                            #self.boardState[coordlist[j][0]][coordlist[j][1]] = rowlist[j]
                        return [True, resultState, [rowlist, coordlist, deleted]]
                return [False]
            else:

                rowlist.append(resultState[y2][x2])

                if x1 > x2: dir[1] = -1
                if x1 < x2: dir[1] = 1
                if y1 == y2: dir[0] = 0
                if y1 > y2: dir[0] = -1
                if y1 < y2: dir[0] = 1

                x1 = x2
                y1 = y2

                # y <= 5

                if y1 < 5 and dir[0] == -1 and dir[1] == -1:
                    x2 = x1 - 1
                elif y1 < 5 and dir[0] == -1 and dir[1] == 1:
                    x2 = x1
                elif y1 < 5 and dir[0] == 1 and dir[1] == 1:
                    x2 = x1 + 1
                elif y1 < 5 and dir[0] == 1 and dir[1] == -1:
                    x2 = x1

                # y >= 5

                elif y1 > 5 and dir[0] == -1 and dir[1] == -1:
                    x2 = x1
                elif y1 > 5 and dir[0] == -1 and dir[1] == 1:
                    x2 = x1 + 1
                elif y1 > 5 and dir[0] == 1 and dir[1] == 1:
                    x2 = x1
                elif y1 > 5 and dir[0] == 1 and dir[1] == -1:
                    x2 = x1 - 1

                # y == 5

                elif y1 == 5 and ((dir[0] == -1 and dir[1] == 1) or (dir[0] == 1 and dir[1] == 1)):
                    x2 = x1
                elif y1 == 5 and ((dir[0] == -1 and dir[1] == -1) or (dir[0] == 1 and dir[1] == -1)):
                    x2 = x1 - 1
                elif y1 == 5 and dir[0] == 1 and dir[1] == 0:
                    x2 = x1 - 1
                elif y1 == 5 and dir[0] == -1 and dir[1] == 0:
                    x2 = x1 - 1
                else:
                    x2 = x1 + dir[1]

                y2 = y1 + dir[0]

                coordlist.append([y2, x2])

    def make_move(self, tab):
        rowlist = tab[0]
        coordlist = tab[1]
        deleted = tab[2]
        self.deleted = deleted
        if deleted == 1:
            self.scoreblack += 1
        elif deleted == 2:
            self.scorewhite += 1
        for i in range(len(rowlist)):
            self.boardState[coordlist[i][0]][coordlist[i][1]] = rowlist[i]


    def generate_moves(self, grid, player):

        all = [[1,0],[0,-1],[0,1],[-1,0]]
        y_less_5 = [[1,1],[-1,-1]] + all
        y_grt_5 = [[-1,1],[1,-1]] + all
        y_eql_5 = [[1,-1],[-1,-1]] + all
        legal_moves = []
        result = []

        for i in range(1,10):
            for j in range(1, len(grid[i]) - 1):
                if grid[i][j] == player:

                    if i > 5:
                        for k in y_grt_5:
                            dx = k[1]
                            dy = k[0]
                            if grid[i + dy][j + dx] != 9:
                                result = self.check_move([i - 1,j- 1],[i + dy- 1, j + dx- 1])
                                if result[0]:
                                    legal_moves.append([result[1],result[2]])

                    elif i < 5:
                        for k in y_less_5:
                            dx = k[1]
                            dy = k[0]
                            if grid[i + dy][j + dx] != 9:
                                result = self.check_move([i - 1,j- 1],[i + dy- 1, j + dx- 1])
                                if result[0]:
                                    legal_moves.append([result[1],result[2]])

                    else:
                        for k in y_eql_5:
                            dx = k[1]
                            dy = k[0]
                            if grid[i + dy][j + dx] != 9:
                                result = self.check_move([i - 1,j- 1],[i + dy- 1, j + dx- 1])
                                if result[0]:
                                    legal_moves.append([result[1],result[2]])
        return legal_moves

    def minimax(self, depth, starting_node, isMaximizingPlayer, alpha, beta):

        if depth == 0:
            return starting_node
        else:
            if isMaximizingPlayer:
                bestNode = Node([],[],float('-inf'),[])
                legal_moves = self.generate_moves(starting_node.grid, 1)

                for move in legal_moves:
                    newNode = Node(move[0], move[1], state_value(move[0], move[1][2], self.turn_counter), [])
                    starting_node.children.append(newNode)
                for node in starting_node.children:
                    nextNode = self.minimax(depth - 1, node, False, alpha, beta)
                    if nextNode.value > bestNode.value:
                        bestNode = nextNode
                    alpha = max(alpha, bestNode.value)
                    if beta <= alpha:
                        break
                return bestNode
            else:
                bestNode = Node([],[],float('inf'),[])
                legal_moves = self.generate_moves(starting_node.grid, 2)

                for move in legal_moves:
                    newNode = Node(move[0], move[1], state_value(move[0], move[1][2], self.turn_counter), [])
                    starting_node.children.append(newNode)
                for node in starting_node.children:
                    nextNode = self.minimax(depth - 1, node, True, alpha, beta)
                    if nextNode.value < bestNode.value:
                        bestNode = nextNode
                    beta = min(beta, bestNode.value)
                    if beta <= alpha:
                        break
                return bestNode
