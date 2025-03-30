import random
import time

class RandomPlayer:
    def __init__(self):
        self.piece_values = {'Elephant': 8,'Lion': 7,'Tiger': 6,'Leopard': 5,'Wolf': 4,'Dog': 3,'Cat': 2,'Rat': 1}
        self.RED_TRAPS = {(0, 2), (0, 4), (1, 3)}
        self.GREEN_TRAPS = {(8, 2), (8, 4), (7, 3)}
        self.RED_DEN = (0, 3)
        self.GREEN_DEN = (8, 3)
        self.WATER_CELLS = {(3, 1), (3, 2), (4, 1), (4, 2), (5, 1), (5, 2), (3, 4), (3, 5), (4, 4), (4, 5), (5, 4), (5, 5)}

    def get_ai_move(self, board, cur_player, depth=None, green_type='human', red_type='human'):
        ai_vs_ai = (green_type == 'ai' and red_type == 'ai')
        if not ai_vs_ai:
            time.sleep(0.5)
        # Get all valid moves
        all_moves = self.get_all_valid_moves(board, cur_player)
        if not all_moves: return None   # Return None if no moves are available
        return random.choice(all_moves) # Return a random move from all moves

    def get_all_valid_moves(self, board, player):
        moves = []
        for row in range(9):
            for col in range(7):
                if board[row][col] is not None and board[row][col].color == player:
                    from_pos = (row, col)
                    valid_moves = self.get_valid_moves(board, from_pos)
                    for to_pos in valid_moves:
                        moves.append((from_pos, to_pos))
        return moves

    def get_valid_moves(self, board, from_pos):
        """Get all valid moves for a piece at a specific position"""
        row, col = from_pos
        piece = board[row][col]
        if piece is None:
            return []
            
        moves = []
        opponent_den = self.GREEN_DEN if piece.color == 'green' else self.RED_DEN
        
        # Check movement based on piece type
        if piece.type == 'Rat':
            # Rat can move in 4 directions and enter water
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 7 and (r, c) != opponent_den:
                    if board[r][c] is None:
                        moves.append((r, c))
                    elif board[r][c].color != piece.color:
                        # Rat can capture elephant or another rat (if not in water)
                        target_piece = board[r][c]
                        if not self.is_water_cell(row, col):  # Rat in water can't capture
                            if (target_piece.type == 'Elephant' or target_piece.type == 'Rat' or 
                                self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(target_piece, r, c)):
                                moves.append((r, c))
        elif piece.type in ['Cat', 'Dog', 'Wolf', 'Leopard', 'Elephant']:
            # Normal move, cannot enter water
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 7 and (r, c) != opponent_den:
                    if not self.is_water_cell(r, c):
                        if board[r][c] is None:
                            moves.append((r, c))
                        elif board[r][c].color != piece.color:
                            # Elephant can't capture rat
                            if piece.type == 'Elephant' and board[r][c].type == 'Rat':
                                continue
                            if self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(board[r][c], r, c):
                                moves.append((r, c))
        elif piece.type in ['Tiger', 'Lion']:
            # Can jump over water
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                # Normal movement
                r, c = row + dr, col + dc
                if 0 <= r < 9 and 0 <= c < 7 and (r, c) != opponent_den:
                    if not self.is_water_cell(r, c):
                        if board[r][c] is None:
                            moves.append((r, c))
                        elif board[r][c].color != piece.color:
                            if self.get_adjusted_rank(piece, row, col) >= self.get_adjusted_rank(board[r][c], r, c):
                                moves.append((r, c))
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

    def get_adjusted_rank(self, piece, row, col):
        if piece.color == 'green' and (row, col) in self.RED_TRAPS: return 0
        elif piece.color == 'red' and (row, col) in self.GREEN_TRAPS: return 0
        return self.piece_values.get(piece.type, 0)

    def is_water_cell(self, row, col): return (row, col) in self.WATER_CELLS