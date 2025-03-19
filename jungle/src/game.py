import pygame 

from const import *
from board import Board

class Game:

    def __init__(self):
        self.board=Board()

    def show_bg(self, surface): #a surface vai ser o self.screen do main.py
        for row in range(rows):
            for col in range(cols):
                if ((row==0 and (col==2 or col==4))or(row==1 and col==3)):#armadilha
                    color = (255, 165, 0)
                elif ((row==8 and (col==2 or col==4))or(row==7 and col==3)):#armadilha
                    color = (255, 165, 0) 
                elif ((row==0 or row==8) and col==3):#casas
                    color = (255, 0, 0)
                elif ((row==3 or row==5) and (col==1 or col==4)):#rio escuro
                    color = (0, 0, 255)
                elif ((row==4 and (col==2 or col==5))):#rio escuro
                    color = (0, 0, 255)
                elif ((row==3 or row==5) and (col==2 or col==5)):#rio claro
                    color = (0, 177, 255, 0.8)
                elif ((row==4) and (col==1 or col==4)):#rio claro
                    color = (0, 177, 255, 0.8)
                elif (row + col) % 2 == 0:
                    color = (234, 235, 200) # verde claro
                else:
                    color = (60, 179, 113) # verde escuro 
                
                rect = (col * sqsize, row * sqsize, sqsize, sqsize) #no pygame o rect tem 4 parametros. (left,top,width,height) o ponto mais em cima e à esquerda + largura + altura 

                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(rows):
            for col in range(cols):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    img=pygame.inage.load(piece.texture)
                    img_center= 
