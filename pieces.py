import pygame

# Importing pieces
black_bishop = pygame.image.load('assets/black_bishop.png')
black_king = pygame.image.load('assets/black_king.png')
black_knight = pygame.image.load('assets/black_knight.png')
black_pawn = pygame.image.load('assets/black_pawn.png')
black_queen = pygame.image.load('assets/black_queen.png')
black_rook = pygame.image.load('assets/black_rook.png')

white_bishop = pygame.image.load('assets/white_bishop.png')
white_king = pygame.image.load('assets/white_king.png')
white_knight = pygame.image.load('assets/white_knight.png')
white_pawn = pygame.image.load('assets/white_pawn.png')
white_queen = pygame.image.load('assets/white_queen.png')
white_rook = pygame.image.load('assets/white_rook.png')

b = [black_bishop, black_king, black_knight, black_pawn, black_queen, black_rook]
w = [white_bishop, white_king, white_knight, white_pawn, white_queen, white_rook]

B = []
W = []

for piece in b:
    B.append(pygame.transform.scale(piece, (55, 55)))

for piece in w:
    W.append(pygame.transform.scale(piece, (55, 55)))

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.idPiece = None
        self.color = color

        self.pawn = False
        self.king = False

        self.selected = False

        self.rows = self.cols = 8
        self.offset = 25

    def get_idPiece(self):
        pass
    
    def get_possible_moves(self, board):
        pass

    def move(self, row, col):
        self.row = row
        self.col = col

    def getCoordinates(self, window):
        x = (window.get_width() // self.rows) * self.col + self.offset
        y = (window.get_height() // self.cols) * self.row + self.offset

        return x, y 
        
    def drawPieces(self, window, board):
        self.get_idPiece()
        if self.color == "w":
            piece = W[self.idPiece]
        elif self.color == "b":
            piece = B[self.idPiece]
        
        x, y = self.getCoordinates(window)

        window.blit(piece, (x, y))

        if self.selected:
            if self.row < 2:
                rect = (x - self.offset + 5, y - self.offset + 5, window.get_width() // self.rows, window.get_width() // self.cols)
            else:
                rect = (x - self.offset, y - self.offset, window.get_width() // self.rows, window.get_width() // self.cols)
            # Drawing selected
            pygame.draw.rect(window, (255, 0, 0), rect, 3)
            # Drawing possible moves --> Debuging purposes
            for move in self.get_possible_moves(board):
                x = (window.get_width() // self.rows) * move[1] + self.offset*2
                y = (window.get_width() // self.cols) * move[0] + self.offset*2
                pygame.draw.circle(window, (0, 0, 255), (x, y), 15)


class Bishop(Piece):
    def get_idPiece(self):
        self.idPiece = 0
    
    def get_possible_moves(self, board):
        moves = []

        # Diagonal Right
        frontRight = 1
        for i in range(self.row + 1, 8):
            if self.col + frontRight < 8:
                if board[i][self.col + frontRight] == 0:
                    moves.append([i, self.col + frontRight])
                elif board[i][self.col + frontRight].color != board[self.row][self.col].color:
                    moves.append([i, self.col + frontRight])
                    break
                elif board[i][self.col + frontRight].color == board[self.row][self.col].color:
                    break
            frontRight += 1
        backRight = 1
        for i in range(self.row - 1, -1, -1):
            if self.col + backRight < 8:
                if board[i][self.col + backRight] == 0:
                    moves.append([i, self.col + backRight])
                elif board[i][self.col + backRight].color != board[self.row][self.col].color:
                    moves.append([i, self.col + backRight])
                    break
                elif board[i][self.col + backRight].color == board[self.row][self.col].color:
                    break
            backRight += 1

        # Diagonal Left
        frontLeft = 1
        for i in range(self.row + 1, 8):
            if self.col - frontLeft > -1:
                if board[i][self.col - frontLeft] == 0:
                    moves.append([i, self.col - frontLeft])
                elif board[i][self.col - frontLeft].color != board[self.row][self.col].color:
                    moves.append([i, self.col - frontLeft])
                    break
                elif board[i][self.col - frontLeft].color == board[self.row][self.col].color:
                    break
            frontLeft += 1
        backLeftt = 1
        for i in range(self.row - 1, -1, -1):
            if self.col - backLeftt > -1:
                if board[i][self.col - backLeftt] == 0:
                    moves.append([i, self.col - backLeftt])
                elif board[i][self.col - backLeftt].color != board[self.row][self.col].color:
                    moves.append([i, self.col - backLeftt])
                    break
                elif board[i][self.col - backLeftt].color == board[self.row][self.col].color:
                    break
            backLeftt += 1


        return moves


class King(Piece):
    def get_idPiece(self):
        self.idPiece = 1
        self.king = True
    
    def get_possible_moves(self, board):
        moves = []

        # Front
        if self.row < 7:
            if board[self.row + 1][self.col] == 0:
                moves.append([self.row + 1, self.col])
            elif board[self.row][self.col].color != board[self.row + 1][self.col].color:
                moves.append([self.row + 1, self.col])
        # Back
        if self.row > 0:
            if board[self.row - 1][self.col] == 0:
                moves.append([self.row - 1, self.col])
            elif board[self.row][self.col].color != board[self.row - 1][self.col].color:
                moves.append([self.row - 1, self.col])
        # Right
        if self.col < 7:
            if board[self.row][self.col + 1] == 0:
                moves.append([self.row, self.col + 1])
            elif board[self.row][self.col].color != board[self.row][self.col + 1].color:
                moves.append([self.row, self.col + 1])
        # Left
        if self.col > 0:
            if board[self.row][self.col - 1] == 0:
                moves.append([self.row, self.col - 1])
            elif board[self.row][self.col].color != board[self.row][self.col - 1].color:
                moves.append([self.row, self.col - 1])
        # Diagonals
        # Right Top
        if self.col < 7:
            if self.row < 7:
                if board[self.row + 1][self.col + 1] == 0:
                    moves.append([self.row + 1, self.col + 1])
                elif board[self.row][self.col].color != board[self.row + 1][self.col + 1].color:
                    moves.append([self.row + 1, self.col + 1])
        # Right Bottom
        if self.col < 7:
            if self.row > 0:
                if board[self.row - 1][self.col + 1] == 0:
                    moves.append([self.row - 1, self.col + 1])
                elif board[self.row][self.col].color != board[self.row - 1][self.col + 1].color:
                    moves.append([self.row - 1, self.col + 1])
        
        # Left Top
        if self.col > 0:
            if self.row < 7:
                if board[self.row + 1][self.col - 1] == 0:
                    moves.append([self.row + 1, self.col - 1])
                elif board[self.row][self.col].color != board[self.row + 1][self.col - 1].color:
                    moves.append([self.row + 1, self.col - 1])
        # left Bottom
        if self.col > 0:
            if self.row > 0:
                if board[self.row - 1][self.col - 1] == 0:
                    moves.append([self.row - 1, self.col - 1])
                elif board[self.row][self.col].color != board[self.row - 1][self.col - 1].color:
                    moves.append([self.row - 1, self.col - 1])

        return moves


class Knight(Piece):
    def get_idPiece(self):
        self.idPiece = 2
    
    def get_possible_moves(self, board):
        moves = []

        # Front Right
        if self.row < 6:
            if self.col < 7:
                if board[self.row + 2][self.col + 1] == 0:
                    moves.append([self.row + 2, self.col + 1])
                elif board[self.row][self.col].color != board[self.row + 2][self.col + 1].color:
                    moves.append([self.row + 2, self.col + 1])
        if self.row < 7:
            if self.col < 6:
                if board[self.row + 1][self.col + 2] == 0:
                    moves.append([self.row + 1, self.col + 2])
                elif board[self.row][self.col].color != board[self.row + 1][self.col + 2].color:
                    moves.append([self.row + 1, self.col + 2])
        
        # Front Left
        if self.row < 6:
            if self.col > 0:
                if board[self.row + 2][self.col - 1] == 0:
                    moves.append([self.row + 2, self.col - 1])
                elif board[self.row][self.col].color != board[self.row + 2][self.col - 1].color:
                    moves.append([self.row + 2, self.col - 1])
        
        if self.row < 7:
            if self.col > 1:
                if board[self.row + 1][self.col - 2] == 0:
                    moves.append([self.row + 1, self.col - 2])
                elif board[self.row][self.col].color != board[self.row + 1][self.col - 2].color:
                    moves.append([self.row + 1, self.col - 2])
        
        # Back Right
        if self.row > 1:
            if self.col < 7:
                if board[self.row - 2][self.col + 1] == 0:
                    moves.append([self.row - 2, self.col + 1])
                elif board[self.row][self.col].color != board[self.row - 2][self.col + 1].color:
                    moves.append([self.row - 2, self.col + 1])
        
        if self.row > 0:
            if self.col < 6:
                if board[self.row - 1][self.col + 2] == 0:
                    moves.append([self.row - 1, self.col + 2])
                elif board[self.row][self.col].color != board[self.row - 1][self.col + 2].color:
                    moves.append([self.row - 1, self.col + 2])
        
        # Back Left
        if self.row > 1:
            if self.col > 0:
                if board[self.row - 2][self.col - 1] == 0:
                    moves.append([self.row - 2, self.col - 1])
                elif board[self.row][self.col].color != board[self.row - 2][self.col - 1].color:
                    moves.append([self.row - 2, self.col - 1])
        if self.row > 0:
            if self.col > 1:
                if board[self.row - 1][self.col - 2] == 0:
                    moves.append([self.row - 1, self.col - 2])
                elif board[self.row][self.col].color != board[self.row - 1][self.col - 2].color:
                    moves.append([self.row - 1, self.col - 2])
        
        return moves


class Pawn(Piece):
    def get_idPiece(self):
        self.idPiece = 3
        self.pawn = True
    
    def get_possible_moves(self, board):
        moves = []
        
        if self.color == 'b':
            if self.row < 2:
                if board[self.row + 2][self.col] == 0 and board[self.row+1][self.col] == 0:
                    moves.append([self.row + 2, self.col])
                    moves.append([self.row + 1, self.col])
                if board[self.row + 1][self.col] == 0:
                    moves.append([self.row + 1, self.col])
            elif self.row < 0:
                if board[self.row + 1][self.col] == 0:
                    moves.append([self.row + 1, self.col])
            
            # Eating
            if self.col < 7:
                if board[self.row + 1][self.col + 1] != 0:
                    if board[self.row + 1][self.col + 1].color != board[self.row][self.col].color:
                        moves.append([self.row + 1, self.col + 1])
            if board[self.row + 1][self.col - 1] != 0:
                if board[self.row + 1][self.col - 1].color != board[self.row][self.col].color:
                    moves.append([self.row + 1, self.col - 1])
        else:
            if self.row > 5:
                if board[self.row - 2][self.col] == 0 and board[self.row - 1][self.col] == 0:
                    moves.append([self.row - 2, self.col])
                    moves.append([self.row - 1, self.col])
                if board[self.row - 1][self.col] == 0:
                    moves.append([self.row - 1, self.col])
            elif self.row > 0:
                if board[self.row - 1][self.col] == 0:
                    moves.append([self.row - 1, self.col])
            
            # Eating
            if self.col < 7:
                if board[self.row - 1][self.col + 1] != 0:
                    if board[self.row - 1][self.col + 1].color != board[self.row][self.col].color:
                        moves.append([self.row - 1, self.col + 1])
            if board[self.row - 1][self.col - 1] != 0:
                if board[self.row - 1][self.col - 1].color != board[self.row][self.col].color:
                    moves.append([self.row - 1, self.col - 1])
        
        return moves


class Queen(Piece):
    def get_idPiece(self):
        self.idPiece = 4
    
    def get_possible_moves(self, board):
        moves = []

        # Diagonal Right
        frontRight = 1
        for i in range(self.row + 1, 8):
            if self.col + frontRight < 8:
                if board[i][self.col + frontRight] == 0:
                    moves.append([i, self.col + frontRight])
                elif board[i][self.col + frontRight].color != board[self.row][self.col].color:
                    moves.append([i, self.col + frontRight])
                    break
                elif board[i][self.col + frontRight].color == board[self.row][self.col].color:
                    break
            frontRight += 1
        backRight = 1
        for i in range(self.row - 1, -1, -1):
            if self.col + backRight < 8:
                if board[i][self.col + backRight] == 0:
                    moves.append([i, self.col + backRight])
                elif board[i][self.col + backRight].color != board[self.row][self.col].color:
                    moves.append([i, self.col + backRight])
                    break
                elif board[i][self.col + backRight].color == board[self.row][self.col].color:
                    break
            backRight += 1

        # Diagonal Left
        frontLeft = 1
        for i in range(self.row + 1, 8):
            if self.col - frontLeft > -1:
                if board[i][self.col - frontLeft] == 0:
                    moves.append([i, self.col - frontLeft])
                elif board[i][self.col - frontLeft].color != board[self.row][self.col].color:
                    moves.append([i, self.col - frontLeft])
                    break
                elif board[i][self.col - frontLeft].color == board[self.row][self.col].color:
                    break
            frontLeft += 1
        backLeftt = 1
        for i in range(self.row - 1, -1, -1):
            if self.col - backLeftt > -1:
                if board[i][self.col - backLeftt] == 0:
                    moves.append([i, self.col - backLeftt])
                elif board[i][self.col - backLeftt].color != board[self.row][self.col].color:
                    moves.append([i, self.col - backLeftt])
                    break
                elif board[i][self.col - backLeftt].color == board[self.row][self.col].color:
                    break
            backLeftt += 1
        
        for i in range(self.row + 1, 8):
            if board[i][self.col] == 0:
                moves.append([i, self.col])
            else:
                if board[i][self.col].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([i, self.col])
                    break
        
        for i in range(self.row - 1, -1, -1):
            if board[i][self.col] == 0:
                moves.append([i, self.col])
            else:
                if board[i][self.col].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([i, self.col])
                    break
        
        for i in range(self.col + 1, 8):
            if board[self.row][i] == 0:
                moves.append([self.row, i])
            else:
                if board[self.row][i].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([self.row, i])
                    break
        
        for i in range(self.col - 1, -1, -1):
            if board[self.row][i] == 0:
                moves.append([self.row, i])
            else:
                if board[self.row][i].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([self.row, i])
                    break

        return moves


class Rook(Piece):
    def get_idPiece(self):
        self.idPiece = 5
    
    def get_possible_moves(self, board):
        moves = []

        for i in range(self.row + 1, 8):
            if board[i][self.col] == 0:
                moves.append([i, self.col])
            else:
                if board[i][self.col].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([i, self.col])
                    break
        
        for i in range(self.row - 1, -1, -1):
            if board[i][self.col] == 0:
                moves.append([i, self.col])
            else:
                if board[i][self.col].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([i, self.col])
                    break
        
        for i in range(self.col + 1, 8):
            if board[self.row][i] == 0:
                moves.append([self.row, i])
            else:
                if board[self.row][i].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([self.row, i])
                    break
        
        for i in range(self.col - 1, -1, -1):
            if board[self.row][i] == 0:
                moves.append([self.row, i])
            else:
                if board[self.row][i].color == board[self.row][self.col].color:
                    break
                else:
                    moves.append([self.row, i])
                    break

        return moves