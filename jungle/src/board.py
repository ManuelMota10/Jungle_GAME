from const import *
from square import Square
from piece import *

class Board:

    def __init__(self):
        self.squares = [[0,0,0,0,0,0,0,0,0] for col in range(cols)]

        self.create()

        self._add_pieces('green')
        self._add_pieces('red')

    def _create(self): #o '_' antes do nome da função signififca que este método só vai ser chamada dentro da class Board
        for row in range (rows):
            for col in range (cols):
                self.squares[row][col] = Square(row,col)


    def _add_pieces(self, color):
    # Definir linhas para cada time (verde/vermelho ou outro par de cores que esteja usando)
        if color == 'green':
            home_row = 8
            second_row = 7
            third_row = 6
        else:  # assumindo que a outra cor é 'red'
            home_row = 0
            second_row = 1
            third_row = 2
    
        self.squares[home_row][3] = Square(home_row, 3, Den(color)) 
    
        trap_positions = [(home_row, 2), (home_row, 4), (home_row-1 if color=='green' else home_row+1, 3)]
        for row, col in trap_positions:
            self.squares[row][col] = Square(row, col, Trap(color))

        animal_positions = [
            (second_row, 0, Elephant(color)),  # Elefante
            (second_row, 6, Lion(color)),      # Leão
            (second_row, 2, Tiger(color)),     # Tigre
            (second_row, 4, Leopard(color)),   # Leopardo
            (third_row, 1, Wolf(color)),       # Lobo
            (third_row, 3, Dog(color)),        # Cão
            (third_row, 5, Cat(color)),        # Gato
            (third_row, 7, Rat(color))         # Rato
        ]
    
        for row, col, piece in animal_positions:
            self.squares[row][col] = Square(row, col, piece)