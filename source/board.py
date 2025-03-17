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
        self.White = (240,217,181)
        self.Brown = (181,136,99)
        self.Blue = (100,149,237)
        self.Orange = (255,165,0)
        self.Red = (200,50,50)
        # wter tiles
        self.w_tiles = {(1,3),(2,3),(4,3),(5,3),(1,4),(2,4),(4,4),(5,4),(1,5),(2,5),(4,5),(5,5)}
        # traps
        self.traps_b = {(2,8),(3,7),(4,8)}    # bottom traps
        self.traps_t = {(2,0),(3,1),(4,0)}    # top traps
        # dens
        self.den_b = (3,0)  # bottom
        self.den_t = (3,8)  # top
        # load images
        self.images = {}
        types = ["den","trap","tiger","lion","elephant","rat","leopard","cat","dog","wolf"]
        for i in types:
            img = pygame.image.load(f"{i}.png")
            img = pygame.transform.smoothscale(img, (self.square, self.square))
            self.images[i] = img                                                        # bot player
            self.images[i + "_flipped"] = pygame.transform.flip(img, False, True)       # top player

    def draw_board(self):
        for r in range(self.row):
            for c in range(self.col):
                # define square colours
                if (c,r) in self.w_tiles: colour = self.Blue
                elif (c,r) == self.den_b or (c,r) == self.den_t: colour = self.Red
                elif (c,r) in self.traps_b or (c,r) in self.traps_t: colour = self.Orange
                elif (r+c) % 2 == 0: colour = self.White
                else: colour = self.Brown
                pygame.draw.rect(self.screen, colour, (c*self.square, r*self.square, self.square, self.square))     # draw square
            trap_img = self.images["trap"]
        for i in self.traps_b | self.traps_t:                          # union of both sets
            x, y = i
            self.screen.blit(trap_img, (x * self.square, y * self.square))

    def draw_animals(self, items):
        for i in items:
            x, y = i["position"]
            name = i["type"]
            player = i["player"]
            img_key = name if player == 1 else name + "_flipped"
            if img_key in self.images: self.screen.blit(self.images[img_key], (x*self.square,y*self.square))
    def run(self):
        items = ["den","tiger","lion","elephant","rat","leopard","cat","dog","wolf"]
        starting_positions_p1 = [(3,8),(0,8),(6,8),(0,6),(6,6),(4,6),(1,7),(5,7),(2,6)]
        starting_positions_p2 = [(3,0),(6,0),(0,0),(6,2),(0,2),(2,2),(5,1),(1,1),(4,2)]
        lst = []
        for i in range(len(items)):
            lst.append({"type": items[i], "position": starting_positions_p1[i], "player": 1})
            lst.append({"type": items[i], "position": starting_positions_p2[i], "player": 2})
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.draw_board()
            self.draw_animals(lst)
            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    game_board = board()
    game_board.run()
