import pygame

from pieces import Bishop, Knight, Rook, Queen, King, Pawn
from AI import AI_chess

class Board:
    def __init__(self, width, height, window):
        self.width = width
        self.height = height
        self.window = window

        self.path = 'assets/'

        self.img = pygame.transform.scale(pygame.image.load(self.path + 'board.png'), (self.width, self.height))

        # game
        self.rows = self.cols = 8
        self.turn = 'w'

        # Create Board
        self.board = [[0 for i in range(self.cols)] for i in range(self.rows)]

        self.board[0][0] = Rook(0, 0, 'b')
        self.board[0][1] = Knight(0, 1, 'b')
        self.board[0][2] = Bishop(0, 2, 'b')
        self.board[0][3] = Queen(0, 3, 'b')
        self.board[0][4] = King(0, 4, 'b')
        self.board[0][5] = Bishop(0, 5, 'b')
        self.board[0][6] = Knight(0, 6, 'b')
        self.board[0][7] = Rook(0, 7, 'b')

        self.board[1][0] = Pawn(1, 0, 'b')
        self.board[1][1] = Pawn(1, 1, 'b')
        self.board[1][2] = Pawn(1, 2, 'b')
        self.board[1][3] = Pawn(1, 3, 'b')
        self.board[1][4] = Pawn(1, 4, 'b')
        self.board[1][5] = Pawn(1, 5, 'b')
        self.board[1][6] = Pawn(1, 6, 'b')
        self.board[1][7] = Pawn(1, 7, 'b')

        self.board[7][0] = Rook(7, 0, 'w')
        self.board[7][1] = Knight(7, 1, 'w')
        self.board[7][2] = Bishop(7, 2, 'w')
        self.board[7][3] = Queen(7, 3, 'w')
        self.board[7][4] = King(7, 4, 'w')
        self.board[7][5] = Bishop(7, 5, 'w')
        self.board[7][6] = Knight(7, 6, 'w')
        self.board[7][7] = Rook(7, 7, 'w')

        self.board[6][0] = Pawn(6, 0, 'w')
        self.board[6][1] = Pawn(6, 1, 'w')
        self.board[6][2] = Pawn(6, 2, 'w')
        self.board[6][3] = Pawn(6, 3, 'w')
        self.board[6][4] = Pawn(6, 4, 'w')
        self.board[6][5] = Pawn(6, 5, 'w')
        self.board[6][6] = Pawn(6, 6, 'w')
        self.board[6][7] = Pawn(6, 7, 'w')

        # AI
        self.Ai_chess = AI_chess(self.board)
    
    def drawBoard(self):
        self.window.blit(self.img, (0, 0))
        self.drawPieces()
    
    def drawPieces(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] != 0:
                    self.board[i][j].drawPieces(self.window, self.board)
    
    def get_selected(self, row, col):
        if self.turn == 'w':
            prev = (-1, -1)
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.board[i][j] != 0:
                        if self.board[i][j].selected:
                            prev = (i, j)
                        self.board[i][j].selected = False
            
            if prev == (-1, -1):
                if self.board[row][col] != 0:
                    if self.board[row][col].color == self.turn:
                        self.board[row][col].selected = True
            else:
                if self.board[row][col] != 0:
                    if self.board[prev[0]][prev[1]].color == self.board[row][col].color:
                        self.board[row][col].selected = True
                    else:
                        self.moving(prev, row, col)
                else:
                    self.moving(prev, row, col)
    
    def change_turn(self):
        if self.turn == 'w':
            self.turn = 'b'
        else:
            self.turn = 'w'
    
    def moving(self, prev, row, col):
        if [row, col] in self.board[prev[0]][prev[1]].get_possible_moves(self.board):
            if not self.kingCheck(prev, row, col):
                self.board[row][col] = self.board[prev[0]][prev[1]]
                self.board[prev[0]][prev[1]].move(row, col)
                self.board[prev[0]][prev[1]] = 0
                self.change_turn()
                if self.checkMate():
                    if self.turn == 'b':
                        print('w wins')
                    else:
                        print('b wins')
                print(self.checkMate())

    def kingCheck(self, prev, row, col):
        board = self.board[:]
        piece = board[row][col]
        board[row][col] = board[prev[0]][prev[1]]
        board[prev[0]][prev[1]].move(row, col)
        board[prev[0]][prev[1]] = 0

        kingPos = []

        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] != 0:
                    if board[i][j].color == self.turn:
                        if board[i][j].king:
                            kingPos = [i, j]

        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] != 0:
                    if board[i][j].color != self.turn:
                        if kingPos in board[i][j].get_possible_moves(board):
                            board[prev[0]][prev[1]] = board[row][col]
                            board[row][col].move(prev[0], prev[1])
                            board[row][col] = piece
                            return True

        board[prev[0]][prev[1]] = board[row][col]
        board[row][col].move(prev[0], prev[1])
        board[row][col] = piece
        
        return False

    def checkMate(self):
        board = self.board[:]
        possible_moves = []

        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] != 0:
                    if board[i][j].color == self.turn:
                        if board[i][j].king:
                            kingPos = [i, j]

        # If for every possible move king stills in check
        for i in range(self.rows):
            for j in range(self.cols):
                if board[i][j] != 0:
                    if board[i][j].color == self.turn:
                        for move in board[i][j].get_possible_moves(board):
                            if not self.kingCheck((i, j), move[0], move[1]):
                                possible_moves.append([move[0], move[1]])
        
        if len(possible_moves) == 0:
            return True
        return False