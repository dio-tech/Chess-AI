import pygame, sys
from board import Board

pygame.init()

class Game:
    def __init__(self):
        # general setup
        self.run = True
        self.width = 750
        self.height = 750
        self.window = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Chess')
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Importing board
        self.board = Board(self.width, self.height, self.window)

    def convertCoordinates(self, x, y):
        row = y // (self.window.get_width()//self.board.cols)
        col = x // (self.window.get_width()//self.board.rows)

        return row, col
        
    def runGame(self):
        while self.run:
            # Draw board
            self.board.drawBoard()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    row, col = self.convertCoordinates(x, y)
                    self.board.get_selected(row, col)
            
            # AI play
            if self.board.turn == 'b':
                prev, row, col = self.board.Ai_chess.move(self.board)
                self.board.moving(prev, row, col)
            
            pygame.display.update()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    game = Game()
    game.runGame()