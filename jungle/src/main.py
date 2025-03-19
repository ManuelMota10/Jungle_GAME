import pygame
import sys 

from const import *
from game import Game 

class Main:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode( (width, height) )
        pygame.display.set_caption('Jungle Game')
        self.game = Game()

    def mainloop(self):

        screen=self.screen
        game=self.game

        while True:
            game.show_bg(screen) #o background tem de aparecer sempre (o ciclo é infinito)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exist()


            pygame.display.update()


main = Main()
main.mainloop()
