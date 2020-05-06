import pygame as pg
from Board import Board
import math
import random
import Colors
from Value import state_value
from Node import Node

pg.init()

MAX, MIN = 10000, -10000

size = (1440, 920)
board_center = (int(size[0]/2 - 250), int(size[1]/2))
ball_r = 32
gap = ball_r/2
dims = [ball_r, gap]
board_lenght = 11*ball_r + 6*gap
current_ball = 0
white_turn = True

screen = pg.display.set_mode(size)
pg.display.set_caption("Abalone")

ended = False
clock = pg.time.Clock()

screen.fill(Colors.WHITE)

board = Board(board_center, board_lenght, screen, dims)
board.initialize()
board.draw(current_ball)

root = Node(board.boardState, [], 0, [])


while not ended:

    if white_turn:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                ended = True

            if event.type == pg.MOUSEBUTTONDOWN:
                 mouse_pos = event.pos
                 for i in range(9):
                    for j in range(len(board.grid[i])):
                        if board.grid[i][j].collidepoint(mouse_pos):
                            if current_ball == 0 and board.boardState[i+1][j+1] == 1:
                                current_ball = [i, j]
                                break
                            elif [i, j] == current_ball:
                                current_ball = 0
                                break
                            elif not board.boardState[i+1][j+1] == 2:
                                result = board.check_move(current_ball, [i, j])
                                if result[0]:
                                    board.make_move(result[2])
                                    white_turn = False
                                    current_ball = 0
                                    break

    if not white_turn:
        board.draw(current_ball)
        pg.display.flip()
        new_move = board.minimax(3, root, False, float('-inf'),float('inf')).move
        board.make_move(new_move)
        root.grid = board.boardState
        root.children = []
        board.turn_counter += 1
        white_turn = True

    if board.deleted == 1 or board.deleted == 2:
        board.deleted = 0
    if board.scorewhite == 6:
        print('White won!')
        ended = True
    if board.scoreblack == 6:
        print('Black won!')
        ended = True

    board.draw(current_ball)
    #board.generate_moves(board.boardState, 2)
    pg.display.flip()

    clock.tick(60)
pg.quit()
