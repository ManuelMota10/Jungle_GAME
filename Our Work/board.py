# board.py
import pygame
from piece import Piece

class Board:
   
    def __init__(self, screen):
        
        self.screen = screen
        self.width = 9 
        self.height = 7  
        self.board = [[None for _ in range(self.width)] for _ in range(self.height)]
        self.square_size = 80
        self.offset_x = (self.screen.get_width() - self.width * self.square_size) // 2
        self.offset_y = (self.screen.get_height() - self.height * self.square_size) // 2
        self.load_images()
        self.setup_board()

    def load_images(self):
        
        self.grass = pygame.image.load("assets/grass.png") 
        self.trap = pygame.image.load("assets/trap.png") 
        self.den = pygame.image.load("assets/den.png") 
        self.river = pygame.image.load("assets/river.png") 
        self.grass = pygame.transform.scale(self.grass, (self.square_size, self.square_size)) # Redimensiona a imagem da grama
        self.trap = pygame.transform.scale(self.trap, (self.square_size, self.square_size)) # Redimensiona a imagem da armadilha
        self.den = pygame.transform.scale(self.den, (self.square_size, self.square_size)) # Redimensiona a imagem da toca
        self.river = pygame.transform.scale(self.river, (self.square_size, self.square_size)) # Redimensiona a imagem do rio

    def setup_board(self):
        
        self.board[0][0] = Piece("Lion", "red", 7)
        self.board[0][6] = Piece("Tiger", "red", 6)
        self.board[0][2] = Piece("Dog", "red", 4)
        self.board[0][4] = Piece("Cat", "red", 3)
        self.board[2][0] = Piece("Rat", "red", 1)
        self.board[2][2] = Piece("Panther", "red", 5)
        self.board[2][4] = Piece("Wolf", "red", 4)
        self.board[2][6] = Piece("Elephant", "red", 8)

        self.board[6][6] = Piece("Lion", "blue", 7)
        self.board[6][0] = Piece("Tiger", "blue", 6)
        self.board[6][4] = Piece("Dog", "blue", 4)
        self.board[6][2] = Piece("Cat", "blue", 3)
        self.board[4][6] = Piece("Rat", "blue", 1)
        self.board[4][4] = Piece("Panther", "blue", 5)
        self.board[4][2] = Piece("Wolf", "blue", 4)
        self.board[4][0] = Piece("Elephant", "blue", 8)
    def draw(self, screen):
        
        for row in range(self.height):
            for col in range(self.width):
                x = col * self.square_size + self.offset_x
                y = row * self.square_size + self.offset_y

                screen.blit(self.grass, (x, y))

                if (row == 1 or row == 2) and (col == 3 or col == 4 or col == 5):
                    screen.blit(self.river, (x, y))
                if (row == 4 or row == 5) and (col == 3 or col == 4 or col == 5):
                    screen.blit(self.river, (x, y))

                if (row == 0 and (col == 3 or col == 5)):
                    screen.blit(self.trap, (x, y))
                if (row == 1 and col == 4):
                    screen.blit(self.trap, (x, y))
                if (row == 6 and (col == 3 or col == 1)):
                    screen.blit(self.trap, (x, y))
                if (row == 5 and col == 2):
                    screen.blit(self.trap, (x, y))

                if row == 0 and col == 3:
                    screen.blit(self.den, (x, y))
                if row == 6 and col == 3:
                    screen.blit(self.den, (x, y))

                piece = self.board[row][col]
                if piece:
                    piece.draw(screen, x, y)

    def get_piece(self, row, col):
     
        if 0 <= row < self.height and 0 <= col < self.width:
            return self.board[row][col]
        else:
            return None 

    def is_valid_move(self, player, start_row, start_col, end_row, end_col):
        
        #print(f"Validando movimento de ({start_row}, {start_col}) para ({end_row}, {end_col})") #debug
        if not (0 <= end_row < self.height and 0 <= end_col < self.width):
            #print("Movimento inválido: fora dos limites do tabuleiro.") #debug
            return False

        piece = self.get_piece(start_row, start_col)
        target_piece = self.get_piece(end_row, end_col)

        if not piece:
            #print("Movimento inválido: nenhuma peça na posição inicial.") #debug
            return False 

        if target_piece and target_piece.color == player.color:
            #print("Movimento inválido: peça da mesma cor na posição final.") #debug
            return False 

        # Regras de movimento (exemplo: apenas uma casa por vez)
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            #print("Movimento inválido: movimento maior que uma casa.") #debug
            return False

        return True

    def move_piece(self, start_row, start_col, end_row, end_col):
       
        piece = self.board[start_row][start_col]
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        print(f"Peça movida de ({start_row}, {start_col}) para ({end_row}, {end_col})") 