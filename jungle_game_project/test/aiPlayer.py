import random
from utils import *

class RandomPlayer:
    def get_ai_move(self, board, current_player):
        valid_moves = []
        #all valid moves
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == current_player:
                    moves = get_valid_moves(piece, row, col, board)
                    for move_row, move_col in moves: valid_moves.append(((row, col), (move_row, move_col)))
        return random.choice(valid_moves) if valid_moves else None

class NegamaxPlayer:
    def get_ai_move(self, board, current_player, depth):
        best_moves = []
        best_score = float('-inf')
        valid_moves = self.get_all_valid_moves(board, current_player)
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)   #make move
            score = -self.negamax(new_board, depth-1, 'green' if current_player == 'red' else 'red')   #get score from negamax
            #add small random factor (+/- 5%)
            # random_factor = 1.0 + (random.random() * 0.1 - 0.05)
            # adjusted_score = score * random_factor
            #update best move if better
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score: best_moves.append(move)
        #choose randomly from best moves, if there are same scores
        return random.choice(best_moves) if best_moves else None
    
    def negamax(self, board, depth, current_player):
        winner = is_game_over(board)
        if winner: return 1000 if winner == current_player else -1000
        if depth == 0: return self.evaluate_board(board, current_player)
        best_score = float('-inf')
        valid_moves = self.get_all_valid_moves(board, current_player)
        if not valid_moves: return -1000    #no moves = loss
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)
            score = -self.negamax(new_board, depth-1, 'green' if current_player == 'red' else 'red')
            best_score = max(best_score, score)
        return best_score
    
    def get_all_valid_moves(self, board, player):
        valid_moves = []
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == player:
                    moves = get_valid_moves(piece, row, col, board)
                    for move_row, move_col in moves: valid_moves.append(((row, col), (move_row, move_col)))
        return valid_moves
    
    def make_temp_move(self, board, move):
        #temporary moves to evaluate moves
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        new_board = [[None for _ in range(7)] for _ in range(9)]
        for r in range(9):
            for c in range(7):
                if board[r][c] is not None:
                    if r == from_row and c == from_col: continue
                    new_board[r][c] = board[r][c]
        new_board[to_row][to_col] = board[from_row][from_col]
        return new_board
    
    def evaluate_board(self, board, player):
        opponent = 'red' if player == 'green' else 'green'
        player_score = self.get_player_score(board, player)
        opponent_score = self.get_player_score(board, opponent)
        return player_score - opponent_score
    
    def get_player_score(self, board, player):
        score = 0
        opponent_den = RED_DEN if player == 'green' else GREEN_DEN
        #check for opponent elephant (RAT)
        is_elephante = any(board[r][c] is not None and board[r][c].color != player and board[r][c].type == 'Elephant'for r in range(9) for c in range(7))
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == player:
                    #base score from piece rank
                    rank = get_adjusted_rank(piece, row, col, board)
                    score += rank * 10
                    #bonus for being close to opponent's den
                    den_distance = abs(row - opponent_den[0]) + abs(col - opponent_den[1])
                    if den_distance < 4:
                        score += (rank - den_distance) * rank
        return score

class AlphaBetaPlayer:
    def __init__(self): self.memory_box = {}  #transposition box
    
    def get_ai_move(self, board, current_player, depth):
        best_moves = []
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        valid_moves = self.get_all_valid_moves(board, current_player)
        
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)
            #get score from alpha-beta
            score = -self.alpha_beta(new_board, depth-1, -beta, -alpha, 'green' if current_player == 'red' else 'red')
            #add small random factor (+/- 5%)
            random_factor = 1.0 + (random.random() * 0.1 - 0.05)
            adjusted_score = score * random_factor
            #update best move if better
            if adjusted_score > best_score:
                best_score = adjusted_score
                best_moves = [move]
            elif adjusted_score == best_score: best_moves.append(move)
            alpha = max(alpha, score)
        #choose randomly from best moves, if there are same scores
        return random.choice(best_moves) if best_moves else None
    
    def alpha_beta(self, board, depth, alpha, beta, current_player):
        #check transposition box
        board_hash = self.hash_board(board)
        if board_hash in self.memory_box and self.memory_box[board_hash]['depth'] >= depth: return self.memory_box[board_hash]['score']
        winner = is_game_over(board)
        if winner: return 1000 if winner == current_player else -1000
        if depth == 0: return self.evaluate_board(board, current_player)
        valid_moves = self.get_all_valid_moves(board, current_player)
        if not valid_moves: return -1000
        best_score = float('-inf')
        next_player = 'green' if current_player == 'red' else 'red'
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)
            score = -self.alpha_beta(new_board, depth-1, -beta, -alpha, next_player)
            best_score = max(best_score, score)
            alpha = max(alpha, score)
            if alpha >= beta: break  #beta cut
        #store in transposition box
        self.memory_box[board_hash] = {'score': best_score, 'depth': depth}
        return best_score
    
    def hash_board(self, board):
        board_str = ""
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece: board_str += f"{row}{col}{piece.color}{piece.type}"
                else: board_str += f"{row}{col}__"
        return board_str
        
    #same as NegamaxPlayer
    def get_all_valid_moves(self, board, player):
        valid_moves = []
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == player:
                    moves = get_valid_moves(piece, row, col, board)
                    for move_row, move_col in moves:
                        valid_moves.append(((row, col), (move_row, move_col)))
        return valid_moves
    
    def make_temp_move(self, board, move):
        from_pos, to_pos = move
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        new_board = [[None for _ in range(7)] for _ in range(9)]
        #copy all pieces except the moving one
        for r in range(9):
            for c in range(7):
                if board[r][c] is not None:
                    if r == from_row and c == from_col: continue  #skip the moving piece
                    new_board[r][c] = board[r][c]
        new_board[to_row][to_col] = board[from_row][from_col]
        return new_board
    
    def evaluate_board(self, board, player):
        opponent = 'red' if player == 'green' else 'green'
        player_score = self.get_player_score(board, player)
        opponent_score = self.get_player_score(board, opponent)
        return player_score - opponent_score
    
    def get_player_score(self, board, player):
        score = 0
        opponent_den = RED_DEN if player == 'green' else GREEN_DEN
        
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == player:
                    rank = get_rank(piece.type)
                    score += rank * 10
                    
                    den_distance = abs(row - opponent_den[0]) + abs(col - opponent_den[1])
                    if den_distance < 4:
                        score += (4 - den_distance) * rank
        
        return score