import random
import time

class Negamax:
    def __init__(self):
        self.piece_values = {'Elephant': 8,'Lion': 7,'Tiger': 6,'Leopard': 5,'Wolf': 4,'Dog': 3,'Cat': 2,'Rat': 1}
        self.RED_TRAPS = {(0, 2), (0, 4), (1, 3)}
        self.GREEN_TRAPS = {(8, 2), (8, 4), (7, 3)}
        self.RED_DEN = (0, 3)
        self.GREEN_DEN = (8, 3)
        self.WATER_CELLS = {(3, 1), (3, 2), (4, 1), (4, 2), (5, 1), (5, 2), (3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (5, 5)}

    def get_ai_move(self, board, cur_player, depth=3, green_type='human', red_type='human'):
        # Add a delay
        ai_vs_ai = (green_type == 'ai' and red_type == 'ai')
        if not ai_vs_ai:
            time.sleep(0.5)
        best_score = float('-inf')
        best_move = None
        best_moves = []
        all_moves = self.get_all_valid_moves(board, cur_player)     # Valid moves
        if not all_moves: return None     # Return none if no moves
        # Check each move
        for from_pos, to_pos in all_moves:
            captured_piece = self.make_move(board, from_pos, to_pos)    # Try a move
            score = -self.negamax(board, depth-1, self.get_opponent(cur_player))       # Evaluate with negamax
            score += random.uniform(-5, 5) # Small random factor
            self.undo_move(board, from_pos, to_pos, captured_piece)     # Undo the move
            # Check the best moves
            if score > best_score: 
                best_score, best_moves= score, [(from_pos, to_pos)]
            elif score == best_score: best_moves.append((from_pos, to_pos))
        return random.choice(best_moves) if best_moves else None     # Return randomly one of the best moves

    def negamax(self, board, depth, player):
        # Check for terminal states
        winner = self.is_game_over(board)
        if winner is not None: return 1000 if winner == player else -1000
        if depth == 0: return self.evaluate_board(board, player)

        max_score = float('-inf')
        all_moves = self.get_all_valid_moves(board, player)
        if not all_moves: return -1000      # If no moves available, player loses
        # Evaluate all possible moves
        for from_pos, to_pos in all_moves:
            captured_piece = self.make_move(board, from_pos, to_pos)        # Make the move
            score = -self.negamax(board, depth-1, self.get_opponent(player))     # Recursive evaluation with negamax
            self.undo_move(board, from_pos, to_pos, captured_piece)         # Undo the move
            max_score = max(max_score, score)
        return max_score

    def evaluate_board(self, board, player):
        opponent = self.get_opponent(player)
        score = 0
        # Count pieces
        player_pieces = []
        opponent_pieces = []
        for row in range(9):
            for col in range(7):
                if board[row][col] is not None:
                    piece, piece_pos= board[row][col], (row, col)
                    if piece.color == player:
                        player_pieces.append((piece, piece_pos))
                        score += self.evaluate_piece(piece, piece_pos, player, board)       # Add piece value
                    else:
                        opponent_pieces.append((piece, piece_pos))
                        score -= self.evaluate_piece(piece, piece_pos, opponent, board)     # Subtract opponent piece value
        
        score += self.evaluate_board_control(board, player, player_pieces, opponent_pieces)     # Evaluate board control
        # Evaluate den threats
        score += self.evaluate_den_threats(board, player, player_pieces)
        score -= self.evaluate_den_threats(board, opponent, opponent_pieces)
        return score

    def evaluate_piece(self, piece, pos, player, board):
        row, col = pos
        value = self.piece_values[piece.type]
        # Adjust value for pieces in opponent's traps
        if (player == 'green' and pos in self.RED_TRAPS) or (player == 'red' and pos in self.GREEN_TRAPS): value *= 0.2  # reduce value for pieces in danger
        # Special case for Rat vs Elephant
        if piece.type == 'Rat':
            # Check if opponent has elephant
            for r in range(9):
                for c in range(7):
                    if board[r][c] is not None and board[r][c].color != player and board[r][c].type == 'Elephant':
                        value += 2  # Rat more valuable if opponent has Elephant
        # Bonus if near opponent's den
        target_den = self.RED_DEN if player == 'green' else self.GREEN_DEN
        distance = abs(row - target_den[0]) + abs(col - target_den[1])
        proximity_bonus = max(0, 10 - distance)  # More bonus for being closer
        value += proximity_bonus
        return value

    def evaluate_board_control(self, board, player, player_pieces, opponent_pieces):
        score = 0
        # water control
        water_control = 0
        for piece, pos in player_pieces:
            if piece.type in ['Rat', 'Tiger', 'Lion']:  water_control += 1      # Pieces that can cross or jump water
        opponent_water_control = 0
        for piece, pos in opponent_pieces:
            if piece.type in ['Rat', 'Tiger', 'Lion']: opponent_water_control += 1
        score += (water_control - opponent_water_control) * 3
        # trap control
        player_trap_control = 0
        opponent_trap_territory = self.RED_TRAPS if player == 'green' else self.GREEN_TRAPS
        
        for piece, pos in player_pieces:
            row, col = pos
            # if any piece near opponent's traps
            for trap in opponent_trap_territory:
                if abs(row - trap[0]) + abs(col - trap[1]) <= 1: player_trap_control += 1
        score += player_trap_control * 5
        # Check mobility
        player_moves = len(self.get_all_valid_moves(board, player))
        score += player_moves * 0.5  # little bonus for having more moves
        return score

    def evaluate_den_threats(self, board, player, player_pieces):
        score = 0
        opponent_den = self.RED_DEN if player == 'green' else self.GREEN_DEN
        for piece, pos in player_pieces:
            row, col = pos
            distance = abs(row - opponent_den[0]) + abs(col - opponent_den[1])
            # Significant threat if piece is close to opponent's den
            if distance <= 2: score += (3 - distance) * 20
            elif distance <= 4: score += (5 - distance) * 5
        return score

    def get_all_valid_moves(self, board, player):
        moves = []
        for row in range(9):
            for col in range(7):
                if board[row][col] is not None and board[row][col].color == player:
                    from_pos = (row, col)
                    valid_moves = self.get_valid_moves(board, from_pos)
                    for to_pos in valid_moves: moves.append((from_pos, to_pos))   
        return moves

    def get_valid_moves(self, board, from_pos):
        row, col = from_pos
        piece = board[row][col]
        if piece is None: return []
        moves = []
        target_den = self.RED_DEN if piece.color == 'green' else self.GREEN_DEN
        opponent_den = self.GREEN_DEN if piece.color == 'green' else self.RED_DEN
        # check each piece movment
        if piece.type == 'Rat':
            # 4 directions and enter water
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 7 and (r, c) != opponent_den:
                    if board[r][c] is None: moves.append((r, c))
                    elif board[r][c].color != piece.color:
                        # Rat can capture elephant or another rat (if not in water)
                        target_piece = board[r][c]
                        if not self.is_water_cell(row, col):  # Rat in water can't capture
                            if (target_piece.type == 'Elephant' or target_piece.type == 'Rat' or self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(target_piece, r, c)):
                                moves.append((r, c))
        elif piece.type in ['Cat', 'Dog', 'Wolf', 'Leopard', 'Elephant']:
            # normal move, cannot enter water
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 7 and (r, c) != opponent_den:
                    if not self.is_water_cell(r, c):
                        if board[r][c] is None: moves.append((r, c))
                        elif board[r][c].color != piece.color:
                            # Elephant can't capture rat
                            if piece.type == 'Elephant' and board[r][c].type == 'Rat': continue
                            if self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(board[r][c], r, c): moves.append((r, c))
        elif piece.type in ['Tiger', 'Lion']:
            # jump over water
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # normal movement
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 7 and (r, c) != opponent_den:
                    if not self.is_water_cell(r, c):
                        if board[r][c] is None: moves.append((r, c))
                        elif board[r][c].color != piece.color:
                            if self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(board[r][c], r, c): moves.append((r, c))
                # Water jump logic
                jump_r, jump_c = row, col
                rat_blocking = False
                while 0 <= jump_r + dr < 9 and 0 <= jump_c + dc < 7:
                    jump_r += dr
                    jump_c += dc
                    if self.is_water_cell(jump_r, jump_c):
                        if board[jump_r][jump_c] is not None and board[jump_r][jump_c].type == 'Rat':
                            rat_blocking = True
                            break
                    else:
                        if not rat_blocking and (jump_r, jump_c) != opponent_den:
                            if board[jump_r][jump_c] is None:
                                moves.append((jump_r, jump_c))
                            elif board[jump_r][jump_c].color != piece.color:
                                if self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(board[jump_r][jump_c], jump_r, jump_c):
                                    moves.append((jump_r, jump_c))
                        break
        return moves

    def get_adjusted_rank(self, piece, row, col, attacker_color=False):
        if piece.color == 'green' and (row, col) in self.RED_TRAPS: return 0
        elif piece.color == 'red' and (row, col) in self.GREEN_TRAPS: return 0
        return self.piece_values.get(piece.type, 0)

    def is_water_cell(self, row, col): return (row, col) in self.WATER_CELLS

    def is_game_over(self, board):
        if board[0][3] is not None and board[0][3].color == 'green': return 'green'
        if board[8][3] is not None and board[8][3].color == 'red': return 'red'
        # Check if any team has no animals left
        green_animals = 0
        red_animals = 0
        for row in range(9):
            for col in range(7):
                if board[row][col] is not None:
                    if board[row][col].color == 'green': green_animals += 1
                    else: red_animals += 1
        
        if green_animals == 0: return 'red'
        if red_animals == 0: return 'green'
        return None  # No winner yet

    def make_move(self, board, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        captured_piece = board[to_row][to_col]
        board[to_row][to_col] = board[from_row][from_col]
        board[from_row][from_col] = None
        return captured_piece

    def undo_move(self, board, from_pos, to_pos, captured_piece):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        board[from_row][from_col] = board[to_row][to_col]
        board[to_row][to_col] = captured_piece

    def get_opponent(self, player): return 'red' if player == 'green' else 'green'
