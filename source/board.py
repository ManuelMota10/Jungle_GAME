import pygame
class board:
    def __init__(self,square=80):
        pygame.init()
        self.col,self.row = 7,9
        self.square = square                                                            # number of squares
        self.width,self.height = self.col*self.square,self.row*self.square              # screen limit
        self.screen = pygame.display.set_mode((self.width, self.height))                # screen size
        pygame.display.set_caption("Jungle Chess")
        # Colours
        self.White = (240, 217, 181)
        self.Brown = (181, 136, 99)
        self.Blue = (100, 149, 237)
        self.Orange = (255, 165, 0)
        self.Red = (200, 50, 50)
        # wter tiles (by rows)
        self.w_tiles = {(1, 3), (2, 3), (4, 3), (5, 3), (1, 4), (2, 4), (4, 4), (5, 4), (1, 5), (2, 5), (4, 5), (5, 5)}
        # traps
        self.traps_b = {(2, 0),(3, 1),(4, 0)}    # bottom traps
        self.traps_t = {(2, 8),(3, 7),(4, 8)}    # top traps
        # dens
        self.den_b = (3, 0)  # bottom
        self.den_t = (3, 8)  # top
    def draw_board(self):
        for r in range(self.row):
            for c in range(self.col):
                # define square colours
                if (c,r) in self.w_tiles: colour = self.Blue
                elif (c,r) == self.den_b or (c, r) == self.den_t: colour = self.Red
                elif (c,r) in self.traps_b or (c, r) in self.traps_t: colour = self.Orange
                elif (r+c) % 2 == 0: colour = self.White
                else: colour = self.Brown
                # draw square
                pygame.draw.rect(self.screen, colour, (c*self.square, r*self.square, self.square, self.square))
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_board()
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game_board = board()
    game_board.run()