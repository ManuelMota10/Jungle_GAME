#game constants
RED_TRAPS = {(0, 2), (0, 4), (1, 3)}
GREEN_TRAPS = {(8, 2), (8, 4), (7, 3)}
RED_DEN = (0, 3)
GREEN_DEN = (8, 3)
WATER_CELLS = {(3, 1), (3, 2), (4, 1), (4, 2), (5, 1), (5, 2), (3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (5, 5)}
ANIMAL_RANKS = {'Elephant': 8, 'Lion': 7, 'Tiger': 6, 'Leopard': 5, 'Wolf': 4, 'Dog': 3, 'Cat': 2, 'Rat': 1}
DIRECTIONS = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def get_rank(animal_type): return ANIMAL_RANKS.get(animal_type, 0)

def get_adjusted_rank(piece, row, col, board):
    #if piece is on enemy's trap
    if piece.color == 'green' and (row, col) in RED_TRAPS: return 0
    elif piece.color == 'red' and (row, col) in GREEN_TRAPS: return 0
    return get_rank(piece.type)

def is_water_cell(row, col): return (row, col) in WATER_CELLS

def is_valid_position(row, col, color):
    if not (0 <= row < 9 and 0 <= col < 7): return False
    #cannot enter own den
    if (color == 'red' and (row, col) == RED_DEN) or (color == 'green' and (row, col) == GREEN_DEN): return False
    return True

def get_valid_moves(piece, row, col, board):
    moves = []
    if piece.type == 'Rat': rat_moves(piece, row, col, moves, board)
    elif piece.type in ['Cat', 'Dog', 'Wolf', 'Leopard']: regular_moves(piece, row, col, moves, board)
    elif piece.type in ['Tiger', 'Lion']: jumping_moves(piece, row, col, moves, board)
    elif piece.type == 'Elephant': elephant_moves(piece, row, col, moves, board)
    return moves

def regular_moves(piece, row, col, moves, board):
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if not is_valid_position(r, c, piece.color) or is_water_cell(r, c): continue
        if board[r][c] is None: moves.append((r, c))
        elif board[r][c].color != piece.color and get_adjusted_rank(piece, row, col, board) >= get_adjusted_rank(board[r][c], r, c, board): moves.append((r, c))

def rat_moves(piece, row, col, moves, board):
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if not is_valid_position(r, c, piece.color): continue
        if board[r][c] is None: moves.append((r, c))
        elif board[r][c].color != piece.color:
            #can capture elephant or another rat
            if (board[r][c].type == 'Elephant' or board[r][c].type == 'Rat' or get_adjusted_rank(piece, row, col, board) >= get_adjusted_rank(board[r][c], r, c, board)) and not is_water_cell(row, col):
                moves.append((r, c))

def elephant_moves(piece, row, col, moves, board):
    for dr, dc in DIRECTIONS:
        r, c = row + dr, col + dc
        if not is_valid_position(r, c, piece.color) or is_water_cell(r, c): continue
        if board[r][c] is None: moves.append((r, c))
        elif board[r][c].color != piece.color and board[r][c].type != 'Rat': moves.append((r, c))  #cannot capture rat

def jumping_moves(piece, row, col, moves, board):
    regular_moves(piece, row, col, moves, board)
    #river jump logic
    for dr, dc in DIRECTIONS:
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
                #make sure can jumped
                if not rat_blocking and (jump_r != row or jump_c != col):  
                    if board[jump_r][jump_c] is None: moves.append((jump_r, jump_c))
                    elif board[jump_r][jump_c].color != piece.color and get_adjusted_rank(piece, row, col, board) >= get_adjusted_rank(board[jump_r][jump_c], jump_r, jump_c, board):
                        moves.append((jump_r, jump_c))
                break

def is_game_over(board):
    #check if any den is occupied
    if board[RED_DEN[0]][RED_DEN[1]] is not None and board[RED_DEN[0]][RED_DEN[1]].color == 'green': return 'green'
    if board[GREEN_DEN[0]][GREEN_DEN[1]] is not None and board[GREEN_DEN[0]][GREEN_DEN[1]].color == 'red': return 'red'
    #count animals of each color
    green_animals = sum(1 for row in board for piece in row if piece is not None and piece.color == 'green')
    red_animals = sum(1 for row in board for piece in row if piece is not None and piece.color == 'red')
    if green_animals == 0: return 'red'  #green no animals, red wins
    if red_animals == 0: return 'green'  #red no animals, green wins
    return None  #no winner yet