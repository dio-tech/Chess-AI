from random import randint
import random

from pkg_resources import cleanup_resources

class AI_chess:
    def __init__(self, board):
        self.board = board
        self.Ai_color = 'b'

    def move(self, class_board):
        # Check if move reduces possible moves of opponent when in check
        b_pieces = []

        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != 0:
                    if self.board[i][j].color == self.Ai_color:
                        if len(self.board[i][j].get_possible_moves(self.board)) != 0:
                            b_pieces.append([i, j])

        move_piece, move = self.get_piece(b_pieces, class_board)

        return move_piece, move[0], move[1]
    
    def get_piece(self, b_pieces, class_board):
        chosen_piece = None
        chosen_move = None
        after_len = [10000]
        equality = [False, None, None]

        b_pieces_possible_moves = []
        for piece in b_pieces:
            b_pieces_possible_moves.append(self.board[piece[0]][piece[1]].get_possible_moves(self.board))

        board = self.board[:]
        possible_moves = []

        # If for every possible move king stills in check
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if board[i][j] != 0:
                    if board[i][j].color != self.Ai_color:
                        for move in board[i][j].get_possible_moves(board):
                            if not class_board.kingCheck((i, j), move[0], move[1]):
                                possible_moves.append([move[0], move[1]])
        
        for piece in b_pieces:
            for movePiece in board[piece[0]][piece[1]].get_possible_moves(board):
                after_possible_moves = []

                piece_moved = board[movePiece[0]][movePiece[1]]
                board[piece[0]][piece[1]].move(movePiece[0], movePiece[1])
                board[movePiece[0]][movePiece[1]] = board[piece[0]][piece[1]]
                board[piece[0]][piece[1]] = 0

                for i in range(len(board)):
                    for j in range(len(board[0])):
                        if board[i][j] != 0:
                            if board[i][j].color != self.Ai_color:
                                for move in board[i][j].get_possible_moves(board):
                                    if not class_board.kingCheck((i, j), move[0], move[1]):
                                        after_possible_moves.append([move[0], move[1]])

                board[piece[0]][piece[1]] = board[movePiece[0]][movePiece[1]]
                board[movePiece[0]][movePiece[1]].move(piece[0], piece[1])
                board[movePiece[0]][movePiece[1]] = piece_moved
                
                if not class_board.kingCheck((piece[0], piece[1]), movePiece[0], movePiece[1]):

                    if len(after_possible_moves) < after_len[-1]:
                        if len(after_possible_moves) < len(possible_moves):
                            after_len.append(len(after_possible_moves))
                            chosen_piece = piece
                            chosen_move = movePiece
                        elif len(after_possible_moves) == after_len[-1]:
                            equality = [True, piece, movePiece]
                        else:
                            chosen_piece = piece
                            chosen_move = movePiece
                else:
                    print('check')
        if equality[0] and len(after_len) == 1:
            chosen_piece = equality[1]
            chosen_move = equality[2]

        return chosen_piece, chosen_move

