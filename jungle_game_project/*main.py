import pygame
import sys

pygame.init()

# Constants
BOARD_W, BOARD_H = 490, 630
TOP_BORDER, REST_BORDER = 50, 80
WIDTH, HEIGHT = BOARD_W+REST_BORDER*2, BOARD_H+TOP_BORDER+REST_BORDER
SQUARE_SIZE = BOARD_W // 7

# Colors
BLACK = (0, 0, 0)
BROWN = (240, 217, 181)
YELLOW = (255, 255, 0)
BLUE = (64, 164, 223)
GREEN = (178, 255, 102)
DARK_GREEN = (0, 100, 0)
RED = (220, 20, 60)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

# Screen state
MAIN_MENU = 0
PLAYER_SELECTION = 1
GAME = 2
current_screen = MAIN_MENU

# Default setting from screen 2
starting_player = 'green'
green_player_type = 'human'
red_player_type = 'human'

# Create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jungle Chess")

# Button class for menu items
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
        # Draw button with hover effect
        color = self.color_on if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border
        # Render text
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
        
    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.is_hovered
        return False

# Jungle animals class
class JungleAnimals:
    def __init__(self, color, type, image):
        self.color = color
        self.type = type
        self.image = pygame.image.load(image)
        self.image = pygame.transform.smoothscale(self.image, (SQUARE_SIZE, SQUARE_SIZE))
        self.has_moved = False

# Initialize the board
board = [[None for _ in range(7)] for _ in range(9)]

# Current Player
current_player = 'green'

# Track selected piece
selected_piece = None
selected_position = None

# Game state
game_over = False
winner = None

# Create buttons for main menu
play_button = Button(WIDTH//2 - 100, HEIGHT//2, 200, 60, "PLAY", DARK_GREEN, BLUE, WHITE)
# Starting player buttons
start_green_button = Button(WIDTH//4 - 100, HEIGHT//2 - 100, 200, 60, "GREEN FIRST", DARK_GREEN, GREEN, WHITE, 28)
start_red_button = Button(3*WIDTH//4 - 100, HEIGHT//2 - 100, 200, 60, "RED FIRST", RED, (255, 100, 100), WHITE, 28)
# Player type buttons - smaller font size
green_human_button = Button(WIDTH//4 - 100, HEIGHT//2 + 50, 200, 60, "GREEN: HUMAN", DARK_GREEN, GREEN, WHITE, 24)
green_ai_button = Button(WIDTH//4 - 100, HEIGHT//2 + 120, 200, 60, "GREEN: AI", DARK_GREEN, GREEN, WHITE, 24)
red_human_button = Button(3*WIDTH//4 - 100, HEIGHT//2 + 50, 200, 60, "RED: HUMAN", RED, (255, 100, 100), WHITE, 24)
red_ai_button = Button(3*WIDTH//4 - 100, HEIGHT//2 + 120, 200, 60, "RED: AI", RED, (255, 100, 100), WHITE, 24)
# Start game button
start_game_button = Button(WIDTH//2 - 100, HEIGHT - 120, 200, 60, "START GAME", BLUE, (100, 200, 255), WHITE, 28)

def init_board():
    # Animals for green (at the bottom)
    board[6][0] = JungleAnimals('green', 'Elephant', 'images/green_Elephant.png')
    board[6][2] = JungleAnimals('green', 'Wolf', 'images/green_Wolf.png')
    board[6][4] = JungleAnimals('green', 'Leopard', 'images/green_Leopard.png')
    board[6][6] = JungleAnimals('green', 'Rat', 'images/green_Rat.png')
    board[7][1] = JungleAnimals('green', 'Cat', 'images/green_Cat.png')
    board[7][5] = JungleAnimals('green', 'Dog', 'images/green_Dog.png')
    board[8][0] = JungleAnimals('green', 'Lion', 'images/green_Lion.png')
    board[8][6] = JungleAnimals('green', 'Tiger', 'images/green_Tiger.png')
    # Animals for red (at the top)
    board[0][0] = JungleAnimals('red', 'Tiger', 'images/red_Tiger.png')
    board[0][6] = JungleAnimals('red', 'Lion', 'images/red_Lion.png')
    board[1][1] = JungleAnimals('red', 'Dog', 'images/red_Dog.png')
    board[1][5] = JungleAnimals('red', 'Cat', 'images/red_Cat.png')
    board[2][0] = JungleAnimals('red', 'Rat', 'images/red_Rat.png')
    board[2][2] = JungleAnimals('red', 'Leopard', 'images/red_Leopard.png')
    board[2][4] = JungleAnimals('red', 'Wolf', 'images/red_Wolf.png')
    board[2][6] = JungleAnimals('red', 'Elephant', 'images/red_Elephant.png')

def get_rank(type):
    ranks = {
        'Elephant': 8,
        'Lion': 7,
        'Tiger': 6,
        'Leopard': 5,
        'Wolf': 4,
        'Dog': 3,
        'Cat': 2,
        'Rat': 1
    }
    return ranks.get(type, 0)

def get_adjusted_rank(piece, row, col, attacker_color=False):
    # Define trap positions
    RED_TRAPS = {(0, 2), (0, 4), (1, 3)}
    GREEN_TRAPS = {(8, 2), (8, 4), (7, 3)}
    # Check if piece is in opponent's trap
    if piece.color == 'green' and (row, col) in RED_TRAPS:
        return 0
    elif piece.color == 'red' and (row, col) in GREEN_TRAPS:
        return 0
    return get_rank(piece.type)

def is_water_cell(row, col):
    water_cells = ((3, 1), (3, 2), (4, 1), (4, 2), (5, 1), (5, 2),(3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (5, 5))
    return (row, col) in water_cells

def get_valid_moves(piece, row, col):
    moves = []
    RED_DEN = (0, 3)
    GREEN_DEN = (8, 3)
    # RAT
    if piece.type == 'Rat':
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 9 and 0 <= c < 7:
                if (piece.color == 'red' and (r, c) == RED_DEN) or (piece.color == 'green' and (r, c) == GREEN_DEN): continue
                if board[r][c] is None:
                    moves.append((r, c))
                elif board[r][c].color != piece.color:
                    # Rat can capture elephant or another rat
                    if (board[r][c].type == 'Elephant' or board[r][c].type == 'Rat' or get_adjusted_rank(piece, row, col) >= get_adjusted_rank(board[r][c], r, c)) and not is_water_cell(row, col):
                        moves.append((r, c))
    # CAT, DOG, WOLF, LEOPARD
    elif piece.type in ['Cat', 'Dog', 'Wolf', 'Leopard']:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 9 and 0 <= c < 7:
                if (piece.color == 'red' and (r, c) == RED_DEN) or (piece.color == 'green' and (r, c) == GREEN_DEN): continue
                if not is_water_cell(r, c):
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != piece.color and get_adjusted_rank(piece, row, col) >= get_adjusted_rank(board[r][c], r, c):
                        moves.append((r, c))
    # TIGER & LION
    elif piece.type in ['Tiger', 'Lion']:
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            # Normal one-step movement
            if 0 <= r < 9 and 0 <= c < 7:
                if (piece.color == 'red' and (r, c) == RED_DEN) or (piece.color == 'green' and (r, c) == GREEN_DEN): continue
                if not is_water_cell(r, c):
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != piece.color and get_adjusted_rank(piece, row, col) >= get_adjusted_rank(board[r][c], r, c):
                        moves.append((r, c))
            # River jump logic
            jump_r, jump_c = row, col
            rat_blocking = False
            while 0 <= jump_r + dr < 9 and 0 <= jump_c + dc < 7:
                jump_r += dr
                jump_c += dc
                if is_water_cell(jump_r, jump_c):
                    if board[jump_r][jump_c] is not None and board[jump_r][jump_c].type == 'Rat':
                        rat_blocking = True
                        break
                else:
                    if not rat_blocking:
                        if board[jump_r][jump_c] is None:
                            moves.append((jump_r, jump_c))
                        elif board[jump_r][jump_c].color != piece.color and get_adjusted_rank(piece, row, col) >= get_adjusted_rank(board[jump_r][jump_c], jump_r, jump_c):
                            moves.append((jump_r, jump_c))
                    break
    # ELEPHANT
    elif piece.type == 'Elephant':
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            r, c = row + dr, col + dc
            if 0 <= r < 9 and 0 <= c < 7:
                if (piece.color == 'red' and (r, c) == RED_DEN) or (piece.color == 'green' and (r, c) == GREEN_DEN): continue
                if not is_water_cell(r, c):
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != piece.color:
                        # Elephant cannot capture rat
                        if board[r][c].type != 'Rat':
                            moves.append((r, c))
    return moves

def is_game_over():
    # Check if either den is occupied
    if board[0][3] is not None and board[0][3].color == 'green':
        return 'green'  
    if board[8][3] is not None and board[8][3].color == 'red':
        return 'red'
    # Check if either team has no animals left
    green_animals = 0
    red_animals = 0
    for row in range(9):
        for col in range(7):
            if board[row][col] is not None:
                if board[row][col].color == 'green':
                    green_animals += 1
                else:
                    red_animals += 1
    if green_animals == 0:
        return 'red'  # Red wins because green has no animals
    if red_animals == 0:
        return 'green'  # Green wins because red has no animals
    return None  # No winner yet

def draw_game_over_message():
    if not game_over or not winner:
        return
    font = pygame.font.SysFont('Arial', 60)
    message = f"{winner.upper()} WINS!"
    text = font.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2))
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(180)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))
    screen.blit(text, text_rect)

def draw_game_screen():
    screen.fill(BROWN)
    # Write title and turn indicator
    title = pygame.font.SysFont("Arial", 36, bold=True)
    text = title.render("Jungle Chess", True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH//2, TOP_BORDER//2)))
    # Turn indicator
    turn_color = DARK_GREEN if current_player == 'green' else RED
    turn_text = pygame.font.SysFont('Arial', 24, bold=True).render(f"{current_player.upper()}'S TURN", True, turn_color)
    screen.blit(turn_text, turn_text.get_rect(center=(WIDTH//2, HEIGHT - REST_BORDER//2)))
    # Draw the game board
    surface = pygame.Surface((BOARD_W, BOARD_H))
    surface.fill(GREEN)
    # Draw water cells
    for row in range(9):
        for col in range(7):
            if is_water_cell(row, col):
                pygame.draw.rect(surface, BLUE, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw den
    pygame.draw.rect(surface, RED, (3 * SQUARE_SIZE, 0, SQUARE_SIZE, SQUARE_SIZE))  # Red den
    pygame.draw.rect(surface, DARK_GREEN, (3 * SQUARE_SIZE, 8 * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))  # Green den
    # Draw traps (Yellow)
    for trap in [(0, 2), (0, 4), (1, 3), (8, 2), (8, 4), (7, 3)]:
        row, col = trap
        pygame.draw.rect(surface, YELLOW, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    # Draw grid
    for row in range(10):
        pygame.draw.line(surface, BLACK, (0, row * SQUARE_SIZE), (BOARD_W, row * SQUARE_SIZE))
    for col in range(8):
        pygame.draw.line(surface, BLACK, (col * SQUARE_SIZE, 0), (col * SQUARE_SIZE, BOARD_H))
    # Draw pieces
    for row in range(9):
        for col in range(7):
            if board[row][col] is not None:
                surface.blit(board[row][col].image, (col * SQUARE_SIZE, row * SQUARE_SIZE))
    screen.blit(surface, (REST_BORDER, TOP_BORDER))
    # Highlight selected piece
    if selected_position:
        row, col = selected_position
        s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
        s.fill((255, 255, 0, 128))  # Semi-transparent yellow
        screen.blit(s, (col * SQUARE_SIZE + REST_BORDER, row * SQUARE_SIZE + TOP_BORDER))
        # Draw possible moves
        if selected_piece:
            valid_moves = get_valid_moves(selected_piece, row, col)
            for move_row, move_col in valid_moves:
                s = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
                s.fill((0, 255, 0, 128))  # Semi-transparent green
                screen.blit(s, (move_col * SQUARE_SIZE + REST_BORDER, move_row * SQUARE_SIZE + TOP_BORDER))
    # Draw game over message if game is over
    if game_over:
        draw_game_over_message()

def draw_main_menu():
    screen.fill(BROWN)
    title_font = pygame.font.SysFont("Arial", 72, bold=True)
    title_text = title_font.render("Jungle Chess", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//3)))
    play_button.rect.centery = HEIGHT//2 + 50
    play_button.rect.centerx = WIDTH//2
    play_button.draw(screen)

def draw_player_selection():
    screen.fill(BROWN)
    # Title
    title_font = pygame.font.SysFont("Arial", 48, bold=True)
    title_text = title_font.render("Game Settings", True, BLACK)
    screen.blit(title_text, title_text.get_rect(center=(WIDTH//2, HEIGHT//8)))
    # Starting player
    subtitle_font = pygame.font.SysFont("Arial", 36)
    subtitle_text = subtitle_font.render("Who goes first?", True, BLACK)
    screen.blit(subtitle_text, subtitle_text.get_rect(center=(WIDTH//2, HEIGHT//4)))
    # Player selection with highlight
    start_green_button.color = DARK_GREEN if starting_player == 'green' else GRAY
    start_red_button.color = RED if starting_player == 'red' else GRAY
    green_human_button.color = DARK_GREEN if green_player_type == 'human' else GRAY
    green_ai_button.color = DARK_GREEN if green_player_type == 'ai' else GRAY
    red_human_button.color = RED if red_player_type == 'human' else GRAY
    red_ai_button.color = RED if red_player_type == 'ai' else GRAY
    # Draw buttons
    start_green_button.draw(screen)
    start_red_button.draw(screen)
    green_human_button.draw(screen)
    green_ai_button.draw(screen)
    red_human_button.draw(screen)
    red_ai_button.draw(screen)
    start_game_button.draw(screen)

def handle_game_click(row, col):
    global selected_piece, selected_position, current_player, game_over, winner
    if game_over:
        return
    # Check human turn
    if (current_player == 'green' and green_player_type != 'human') or \
       (current_player == 'red' and red_player_type != 'human'):
        return  # no clicks if is AI
    # adjust the border
    col = col - REST_BORDER
    row = row - TOP_BORDER
    if 0 <= col < BOARD_W and 0 <= row < BOARD_H:
        col = col // SQUARE_SIZE
        row = row // SQUARE_SIZE
        if selected_piece is None:
            # Select a piece
            if board[row][col] is not None and board[row][col].color == current_player:
                selected_piece = board[row][col]
                selected_position = (row, col)
        else:
            # Move the selected piece
            valid_moves = get_valid_moves(selected_piece, selected_position[0], selected_position[1])
            if (row, col) in valid_moves:
                # Move the piece
                board[row][col] = selected_piece
                board[selected_position[0]][selected_position[1]] = None
                # Switch player
                current_player = 'red' if current_player == 'green' else 'green'
                # Check for game over
                winner = is_game_over()
                if winner:
                    game_over = True
            # Deselect piece
            selected_piece = None
            selected_position = None

def update_menu_buttons(mouse_pos):
    if current_screen == MAIN_MENU:
        play_button.update(mouse_pos)
    elif current_screen == PLAYER_SELECTION:
        start_green_button.update(mouse_pos)
        start_red_button.update(mouse_pos)
        green_human_button.update(mouse_pos)
        green_ai_button.update(mouse_pos)
        red_human_button.update(mouse_pos)
        red_ai_button.update(mouse_pos)
        start_game_button.update(mouse_pos)

def main():
    global current_screen, current_player, starting_player, green_player_type, red_player_type, game_over, selected_piece, selected_position
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        update_menu_buttons(mouse_pos)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if current_screen == MAIN_MENU:
                if play_button.is_clicked(event):
                    current_screen = PLAYER_SELECTION
            elif current_screen == PLAYER_SELECTION:
                if start_green_button.is_clicked(event):
                    starting_player = 'green'
                elif start_red_button.is_clicked(event):
                    starting_player = 'red'
                elif green_human_button.is_clicked(event):
                    green_player_type = 'human'
                elif green_ai_button.is_clicked(event):
                    green_player_type = 'ai'
                elif red_human_button.is_clicked(event):
                    red_player_type = 'human'
                elif red_ai_button.is_clicked(event):
                    red_player_type = 'ai'
                elif start_game_button.is_clicked(event):
                    current_screen = GAME
                    init_board()
                    current_player = starting_player
                    game_over = False
                    selected_piece = None
                    selected_position = None
            elif current_screen == GAME:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    handle_game_click(pos[1], pos[0])  # y, x coordinates
        # Draw the appropriate screen
        if current_screen == MAIN_MENU:
            draw_main_menu()
        elif current_screen == PLAYER_SELECTION:
            draw_player_selection()
        elif current_screen == GAME:
            draw_game_screen()
        pygame.display.update()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
