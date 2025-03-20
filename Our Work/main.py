# game.py
import pygame
from board import Board
from player import Player
from ai import AIPlayer # Descomente quando tivermos a IA

class Game:
   
    def __init__(self):
        
        pygame.init() 
        self.screen_width = 630 
        self.screen_height = 560 
        self.square_size = 80 
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height)) 
        pygame.display.set_caption("Animal Chess") 
        self.clock = pygame.time.Clock() 
        self.board = Board(self.screen) 
        self.player1 = Player("Player 1", "red") 
        self.player2 = Player("Player 2", "blue") 
        self.current_player = self.player1 
        self.selected_piece = None 
        self.running = True 

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False 
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                row = mouse_pos[1] // self.square_size 
                col = mouse_pos[0] // self.square_size 
                self.select_piece(row, col)
    def select_piece(self, row, col):
       
        piece = self.board.get_piece(row, col)

        if piece and piece.color == self.current_player.color:
            self.selected_piece = (row, col)
            print(f"Peça selecionada: {piece.name} ({row}, {col})")
        elif self.selected_piece:
            
            start_row, start_col = self.selected_piece
            if self.board.is_valid_move(self.current_player, start_row, start_col, row, col):
                self.board.move_piece(start_row, start_col, row, col) 
                self.selected_piece = None 
                self.switch_player() 
            else:
                print("Movimento inválido!")
    def switch_player(self):
       
        if self.current_player == self.player1:
            self.current_player = self.player2
        else:
            self.current_player = self.player1
        print(f"Vez do jogador: {self.current_player.name} ({self.current_player.color})")
    def update(self):
        
        pass 
    def render(self):
      
        self.screen.fill((255, 255, 255)) 
        self.board.draw(self.screen)  
        pygame.display.flip()  
    def run(self):
        
        while self.running:
            self.handle_input() 
            self.update() 
            self.render() 
            self.clock.tick(60) 
        pygame.quit() 
if __name__ == "__main__":
    game = Game()
    game.run()