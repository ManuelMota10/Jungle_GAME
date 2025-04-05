import pygame
import sys
from aiPlayer import NegamaxPlayer, RandomPlayer, AlphaBetaPlayer
from utils import get_valid_moves, RED_DEN, GREEN_DEN, RED_TRAPS, GREEN_TRAPS, WATER_CELLS, ANIMAL_RANKS, is_game_over, get_rank

pygame.init()
#constants
BOARD_W, BOARD_H = 490, 630
TOP_BORDER, REST_BORDER = 50, 80
WIDTH, HEIGHT = BOARD_W+REST_BORDER*2, BOARD_H+TOP_BORDER+REST_BORDER
SQUARE_SIZE = BOARD_W // 7
#colours
BLACK = (0, 0, 0)
BROWN = (240, 217, 181)
YELLOW = (255, 255, 0)
BLUE = (64, 164, 223)
GREEN = (178, 255, 102)
DARK_GREEN = (0, 100, 0)
RED = (220, 20, 60)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
#screen state
MAIN_MENU, PLAYER_SELECTION, GAME = 0, 1, 2
current_screen = MAIN_MENU
#default setting, screen 2
starting_player, green_player_type, red_player_type= 'green', 'human', 'human'
#initialize AI
nega = NegamaxPlayer()
rand = RandomPlayer()
ab = AlphaBetaPlayer()
#create window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Chess")

class JungleAnimals:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

class Button:
    def __init__(self, x, y, width, height, text, color, color_on, text_color=BLACK, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.color_on = color_on
        self.text_color = text_color
        self.font = pygame.font.SysFont("Arial", font_size, bold=True)
        self.is_hovered = False
        
    def draw(self, surface):
        #draw button
        color = self.color_on if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  #border
        #text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def update(self, mouse_pos): self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: return self.is_hovered
        return False

#main menu buttons
play_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 60, "PLAY", DARK_GREEN, BLUE, WHITE)
green_human_button = Button(WIDTH//4 - 100, HEIGHT//2 - 200, 200, 60, "HUMAN", DARK_GREEN, GREEN, WHITE, 24)
green_random_button = Button(WIDTH//4 - 100, HEIGHT//2 - 100, 200, 60, "RANDOM", DARK_GREEN, GREEN, WHITE, 24)
green_negamax_button = Button(WIDTH//4 - 100, HEIGHT//2, 200, 60, "NEGAMAX", DARK_GREEN, GREEN, WHITE, 24)
green_ab_button = Button(WIDTH//4 - 100, HEIGHT//2 + 100, 200, 60, "ALPHA-BETA", DARK_GREEN, GREEN, WHITE, 24)
red_human_button = Button(3*WIDTH//4 - 100, HEIGHT//2 - 200, 200, 60, "HUMAN", RED, (255, 100, 100), WHITE, 24)
red_random_button = Button(3*WIDTH//4 - 100, HEIGHT//2 - 100, 200, 60, "RANDOM", RED, (255, 100, 100), WHITE, 24)
red_negamax_button = Button(3*WIDTH//4 - 100, HEIGHT//2, 200, 60, "NEGAMAX", RED, (255, 100, 100), WHITE, 24)
red_ab_button = Button(3*WIDTH//4 - 100, HEIGHT//2 + 100, 200, 60, "ALPHA-BETA", RED, (255, 100, 100), WHITE, 24)
start_game_button = Button(WIDTH//2 - 100, HEIGHT - 150, 200, 60, "START GAME", BLUE, (100, 200, 255), WHITE, 28)
#font and size
title_font_large = pygame.font.SysFont("Arial", 72, bold=True)
title_font_medium = pygame.font.SysFont("Arial", 48, bold=True)
title_font_small = pygame.font.SysFont("Arial", 36, bold=True)
turn_font = pygame.font.SysFont('Arial', 24, bold=True)
game_over_font = pygame.font.SysFont('Arial', 60)
#inicial board and game state
board = [[None for _ in range(7)] for _ in range(9)]
current_player = 'green'
selected_piece = None
selected_position = None
game_over = False
winner = None

def init_board():
    global board
    board = [[None for _ in range(7)] for _ in range(9)]    #reset the board
    #initial positions
    animal_positions = {('green', 'Elephant'): (6, 0),# Green animals (bottom)
                        ('green', 'Wolf'): (6, 2),
                        ('green', 'Leopard'): (6, 4),
                        ('green', 'Rat'): (6, 6),
                        ('green', 'Cat'): (7, 1),
                        ('green', 'Dog'): (7, 5),
                        ('green', 'Lion'): (8, 0),
                        ('green', 'Tiger'): (8, 6),
                        ('red', 'Tiger'): (0, 0),     # Red animals (top)
                        ('red', 'Lion'): (0, 6),
                        ('red', 'Dog'): (1, 1),
                        ('red', 'Cat'): (1, 5),
                        ('red', 'Rat'): (2, 0),
                        ('red', 'Leopard'): (2, 2),
                        ('red', 'Wolf'): (2, 4),
                        ('red', 'Elephant'): (2, 6)}
    #put animals on the board
    for (color, type), (row, col) in animal_positions.items(): 
        board[row][col] = JungleAnimals(color, type, f'images/{color}_{type}.png')

def draw_game_over_message():
    if not game_over or not winner: return
    message = f"{winner.upper()} WINS!"
    text = game_over_font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    #semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)

def draw_game_screen(): #screen 3, game screen
    screen.fill(BROWN)
    #title
    text = title_font_small.render("Jungle Chess", True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH//2, TOP_BORDER//2)))
    #turn indicator
    turn_color = DARK_GREEN if current_player == 'green' else RED
    turn_text = turn_font.render(f"{current_player.upper()}'S TURN", True, turn_color)
    screen.blit(turn_text, turn_text.get_rect(center=(WIDTH//2, HEIGHT - REST_BORDER//2)))
    #board surface
    surface = pygame.Surface((BOARD_W, BOARD_H))
    surface.fill(GREEN)
    #water cells
    for row, col in WATER_CELLS: pygame.draw.rect(surface, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    #dens
    pygame.draw.rect(surface, RED, (RED_DEN[1] * SQUARE_SIZE, RED_DEN[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Red den
    pygame.draw.rect(surface, DARK_GREEN, (GREEN_DEN[1] * SQUARE_SIZE, GREEN_DEN[0] * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Green den
    #traps
    for row, col in RED_TRAPS.union(GREEN_TRAPS): pygame.draw.rect(surface, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    #grid
    for row in range(10): pygame.draw.line(surface, BLACK, (0, row * SQUARE_SIZE), (BOARD_W, row * SQUARE_SIZE))
    for col in range(8): pygame.draw.line(surface, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, BOARD_H))
    #pieces
    for row in range(9):
        for col in range(7):
            if board[row][col] is not None:
                surface.blit(board[row][col].image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    screen.blit(surface, (REST_BORDER, TOP_BORDER))
    #highlight selected piece
    if selected_position:
        row, col = selected_position
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill((255, 255, 0, 128))  #transparent yellow
        screen.blit(s, (col * SQUARE_SIZE + REST_BORDER, row * SQUARE_SIZE + TOP_BORDER))
        #draw possible moves for the selected piece
        if selected_piece:
            valid_moves = get_valid_moves(selected_piece, row, col, board)
            for move_row, move_col in valid_moves:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill((0, 255, 0, 128))  # Transparent green
                screen.blit(s, (move_col * SQUARE_SIZE + REST_BORDER, move_row * SQUARE_SIZE + TOP_BORDER))
    if game_over: draw_game_over_message() #output game over message

def draw_player_selection():    #screen 2, selection screen
    screen.fill(BROWN)
    #title
    title_text = title_font_medium.render("Game Settings", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//8)))
    #player selection with highlight
    green_human_button.color = DARK_GREEN if green_player_type == 'human' else GRAY
    green_negamax_button.color = DARK_GREEN if green_player_type == 'negamax' else GRAY
    green_random_button.color = DARK_GREEN if green_player_type == 'random' else GRAY
    green_ab_button.color = DARK_GREEN if green_player_type == 'alpha-beta' else GRAY
    red_human_button.color = RED if red_player_type == 'human' else GRAY
    red_negamax_button.color = RED if red_player_type == 'negamax' else GRAY
    red_random_button.color = RED if red_player_type == 'random' else GRAY
    red_ab_button.color = RED if red_player_type == 'alpha-beta' else GRAY
    # Draw all buttons
    green_human_button.draw(screen)
    green_negamax_button.draw(screen)
    green_random_button.draw(screen)
    green_ab_button.draw(screen)
    red_human_button.draw(screen)
    red_negamax_button.draw(screen)
    red_random_button.draw(screen)
    red_ab_button.draw(screen)
    start_game_button.draw(screen)

def draw_main_menu():   #screen 1, menu screen
    screen.fill(BROWN)
    title_text = title_font_large.render("Jungle Chess", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//3)))
    play_button.rect.centery = HEIGHT//2 + 50
    play_button.rect.centerx = WIDTH//2
    play_button.draw(screen)

def draw_main_menu():
    screen.fill(BROWN)
    title_text = title_font_large.render("Jungle Chess", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//3)))
    play_button.rect.centery = HEIGHT//2 + 50
    play_button.rect.centerx = WIDTH//2
    play_button.draw(screen)

def handle_game_click(row, col):
    global selected_piece, selected_position, current_player, game_over, winner
    if game_over: return
    #check if human player
    if (current_player == 'green' and green_player_type != 'human') or (current_player == 'red' and red_player_type != 'human'): return  #no clicks if is AI pla
    #adjust for borders
    col_adjusted = (col - REST_BORDER) // SQUARE_SIZE
    row_adjusted = (row - TOP_BORDER) // SQUARE_SIZE
    #check if clicked inside the board
    if 0 <= col_adjusted < 7 and 0 <= row_adjusted < 9:
        if selected_piece is None:
            #select piece
            if board[row_adjusted][col_adjusted] is not None and board[row_adjusted][col_adjusted].color == current_player:
                selected_piece = board[row_adjusted][col_adjusted]
                selected_position = (row_adjusted, col_adjusted)
        else:
            valid_moves = get_valid_moves(selected_piece, selected_position[0], selected_position[1], board)
            if (row_adjusted, col_adjusted) in valid_moves:
                #make the move
                board[row_adjusted][col_adjusted] = selected_piece
                board[selected_position[0]][selected_position[1]] = None
                current_player = 'red' if current_player == 'green' else 'green'  # Switch player
                #check if game is over
                winner = is_game_over(board)
                if winner: game_over = True
            #deselect piece
            selected_piece = None
            selected_position = None

def update_menu_buttons(mouse_pos):  
    #update buttons
    if current_screen == MAIN_MENU: play_button.update(mouse_pos)
    elif current_screen == PLAYER_SELECTION:
        green_human_button.update(mouse_pos)
        green_negamax_button.update(mouse_pos)
        green_random_button.update(mouse_pos)
        green_ab_button.update(mouse_pos)
        red_human_button.update(mouse_pos)
        red_negamax_button.update(mouse_pos)
        red_random_button.update(mouse_pos)
        red_ab_button.update(mouse_pos)
        start_game_button.update(mouse_pos)

def ai_turn():
    global current_player, game_over, winner, board
    if game_over: return
    #check if is AI turn
    is_ai_turn = ((current_player == 'green' and green_player_type in ['negamax', 'random', 'alpha-beta']) or 
                 (current_player == 'red' and red_player_type in ['negamax', 'random', 'alpha-beta']))
    if is_ai_turn:
        ai_type = green_player_type if current_player == 'green' else red_player_type
        ai_move = None
        #get AI move
        if ai_type == 'random': ai_move = rand.get_ai_move(board, current_player, green_type=green_player_type, red_type=red_player_type)
        else:
            #adjust the depth for negamax and alpha-beta
            total_pieces = sum(1 for row in board for piece in row if piece is not None)
            depth = 3 if total_pieces > 10 else 5
            if ai_type == 'alpha-beta':
                ai_move = ab.get_ai_move(board, current_player, depth, green_player_type, red_player_type)
                ab.memory_box.clear()  #clear memory to process faster
            else: ai_move = nega.get_ai_move(board, current_player, depth, green_player_type, red_player_type)  #negamax
        #AI moves
        if ai_move:
            from_pos, to_pos = ai_move
            from_row, from_col = from_pos
            to_row, to_col = to_pos
            #make moves
            board[to_row][to_col] = board[from_row][from_col]
            board[from_row][from_col] = None
            current_player = 'red' if current_player == 'green' else 'green'  #switch player
            #check if game is over
            winner = is_game_over(board)
            if winner:game_over = True

def main():
    global current_screen, current_player, starting_player, green_player_type, red_player_type, game_over, selected_piece, selected_position
    clock = pygame.time.Clock()
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        update_menu_buttons(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            if current_screen == MAIN_MENU:
                if play_button.is_clicked(event): current_screen = PLAYER_SELECTION
            #selection of AI or player
            elif current_screen == PLAYER_SELECTION:
                #green
                if green_human_button.is_clicked(event): green_player_type = 'human'
                elif green_negamax_button.is_clicked(event): green_player_type = 'negamax'
                elif green_random_button.is_clicked(event): green_player_type = 'random'
                elif green_ab_button.is_clicked(event): green_player_type = 'alpha-beta'
                #red
                elif red_human_button.is_clicked(event): red_player_type = 'human'
                elif red_negamax_button.is_clicked(event): red_player_type = 'negamax'
                elif red_random_button.is_clicked(event): red_player_type = 'random'
                elif red_ab_button.is_clicked(event):red_player_type = 'alpha-beta'
                #start game
                elif start_game_button.is_clicked(event):
                    current_screen = GAME
                    init_board()
                    current_player = starting_player
                    game_over = False
                    selected_piece = None
                    selected_position = None
            #in game
            elif current_screen == GAME and event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                handle_game_click(pos[1], pos[0])  # y, x coordinates
        if current_screen == GAME: ai_turn()  #make AI turn if needed
        #draw the right screen
        if current_screen == MAIN_MENU: draw_main_menu()
        elif current_screen == PLAYER_SELECTION: draw_player_selection()
        elif current_screen == GAME: draw_game_screen()
        pygame.display.update()
        clock.tick(60)  #limit at 60 fps
    pygame.quit()
    sys.exit()

if __name__ == "__main__": main()