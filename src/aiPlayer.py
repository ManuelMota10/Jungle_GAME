import random
from utils import *

class AIPlayer:
    #all legal and possible moves
    def get_all_valid_moves(self, board, player):
        valid_moves = []
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == player:
                    moves = get_valid_moves(piece, row, col, board)
                    for move_row, move_col in moves:
                        if is_valid_position(move_row, move_col, piece.color): valid_moves.append(((row, col), (move_row, move_col)))
        return valid_moves
    
    def make_temp_move(self, board, move):
        #unpacking
        from_pos, to_pos = move
        from_row, from_col = from_pos   #source position
        to_row, to_col = to_pos         #destination pos
        #create a copy of the board
        new_board = [row[:] for row in board]
        #move the piece
        new_board[to_row][to_col] = board[from_row][from_col]
        new_board[from_row][from_col] = None
        return new_board
    
    def evaluate_board(self, board, player):
        opponent = 'red' if player == 'green' else 'green'
        player_score = self.get_player_score(board, player)
        opponent_score = self.get_player_score(board, opponent)
        #check if player can directly capture den
        opponent_den = RED_DEN if player == 'green' else GREEN_DEN
        player_den = GREEN_DEN if player == 'green' else RED_DEN
        den_row, den_col = opponent_den
        #check for den capture opportunity
        for r in range(9):
            for c in range(7):
                piece = board[r][c]
                if piece and piece.color == player:
                    valid_moves = get_valid_moves(piece, r, c, board)
                    if (den_row, den_col) in valid_moves: return 5000  #immediate win
        #calculate den threats and mobility
        ply_den_threat = self.is_den_threat(board, player, opponent_den)
        op_den_threat = self.is_den_threat(board, opponent, player_den)
        mobility_score = 0
        return (player_score - opponent_score) + (ply_den_threat * 2) - (op_den_threat * 1.5) + (mobility_score * 0.5)
    
    def get_player_score(self, board, player):
        score = 0
        opponent_den = RED_DEN if player == 'green' else GREEN_DEN
        den_row, den_col = opponent_den     #den coordinaate
        #check for opponent elephant (for rat value calculation)
        is_elephant = False
        for r in range(9):
            for c in range(7):
                piece = board[r][c]
                if piece and piece.color != player and piece.type == 'Elephant':
                    is_elephant = True
                    break
            if is_elephant: break
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                if piece and piece.color == player:
                    #base score from piece rank
                    rank = get_adjusted_rank(piece, row, col)
                    #special case: rat vs elephant
                    if piece.type == 'Rat' and is_elephant: score += 15  #increase rat value when opponent has elephant
                    else: score += rank * 10
                    #bonus for being close to opponent's den
                    den_distance = abs(row - den_row) + abs(col - den_col)
                    if den_distance < 6: score += (6 - den_distance) * rank
        return score
    
    def is_den_threat(self, board, player, op_den):
        den_row, den_col = op_den   #opponent den position
        threat_score = 0            #threat level
        #distance to opponent den
        for row in range(max(0, den_row-2), min(9, den_row+3)):
            for col in range(max(0, den_col-2), min(7, den_col+3)):
                piece = board[row][col]
                if piece and piece.color == player:
                    distance = abs(row - den_row) + abs(col - den_col)
                    if distance <= 2: threat_score += (3 - distance) * get_rank(piece.type) * 3
        return threat_score

class RandomPlayer(AIPlayer):
    def get_ai_move(self, board, current_player):
        valid_moves = self.get_all_valid_moves(board, current_player)
        return random.choice(valid_moves) if valid_moves else None

class NegamaxPlayer(AIPlayer):
    def get_ai_move(self, board, current_player, depth):
        best_moves = []
        best_score = float('-inf')
        valid_moves = self.get_all_valid_moves(board, current_player)
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)    #tmp board, not to change on main one
            #negamax recursively, evaluate the score
            score = -self.negamax(new_board, depth-1, 'green' if current_player == 'red' else 'red')
            if score > best_score:
                best_score = score
                best_moves = [move]
            elif score == best_score: best_moves.append(move)
        return random.choice(best_moves) if best_moves else None
    
    def negamax(self, board, depth, current_player):
        #check if game is over
        winner = is_game_over(board)
        if winner: return 1000 if winner == current_player else -1000
        #base case for recursive negamax
        if depth == 0: return self.evaluate_board(board, current_player)
        best_score = float('-inf')
        valid_moves = self.get_all_valid_moves(board, current_player)
        #no moves = loss
        if not valid_moves: return -1000
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)
            score = -self.negamax(new_board, depth-1, 'green' if current_player == 'red' else 'red')
            best_score = max(best_score, score)
        return best_score


class AlphaBetaPlayer(AIPlayer):
    def __init__(self): 
        self.memory_box = {}    #store previous evaluated positions to avoid recalculation
        self.killer_moves = {}  #killer heuristic, remeber non-capture moves that cause AB cuts
        self.move_hist = {}     #history heuristic, track successful moves

    def get_ai_move(self, board, current_player, depth):
        self.killer_moves = {}  #reset killer dict
        best_moves = []
        best_score = float('-inf')
        alpha = float('-inf')    #alfa initial stae
        beta = float('inf')      #beta initial state
        valid_moves = self.get_all_valid_moves(board, current_player)
        #sorts moves to optimize AB search
        valid_moves = self.order_moves(valid_moves, board, current_player, 0)
        next_player = 'green' if current_player == 'red' else 'red'
        #iterative deepening, search increasingly deeper levels
        for cur_depth in range(2, depth + 1):
            cur_best_score = float('-inf')
            cur_best_moves = []
            for move in valid_moves:
                new_board = self.make_temp_move(board, move)    #tmp new board
                #call negamax with AB cuts
                score = -self.alpha_beta(new_board, depth-1, -beta, -alpha, next_player, 1)
                if score > cur_best_score:      #update best score and move
                    cur_best_score = score
                    cur_best_moves = [move]
                elif score == cur_best_score: cur_best_moves.append(move)
                alpha = max(alpha, score)
                #update history, 2^cur_depth, give more weight to successful deep moves
                move_key = f"{move[0][0]},{move[0][1]}-{move[1][0]},{move[1][1]}"
                if move_key not in self.move_hist: self.move_hist[move_key] = 0
                self.move_hist[move_key] += 2 ** cur_depth
            best_score, best_moves = cur_best_score, cur_best_moves
            #early winning move, stop searching if found winning move
            if best_score > 900: break  
        return random.choice(best_moves) if best_moves else None
    
    def order_moves(self, moves, board, player, depth):
        scored_moves = []
        for move in moves:
            from_pos, to_pos = move
            to_row, to_col = to_pos
            score = 0
            #prioritize captures, especially high-value pieces
            if board[to_row][to_col] is not None: score += get_rank(board[to_row][to_col].type) * 10
            #killer move heuristic, 900 bonus
            if move in self.killer_moves.get(depth, []): score += 900
            #history heuristic, add few points for previous success move
            move_key = f"{move[0][0]},{move[0][1]}-{move[1][0]},{move[1][1]}"
            if move_key in self.move_hist: score += self.move_hist[move_key] // 10
            #prefer moves toward opponent's den
            from_row, from_col = from_pos
            opponent_den = RED_DEN if player == 'green' else GREEN_DEN
            den_row, den_col = opponent_den
            #current distance vs. new distance
            cur_dist = abs(from_row - den_row) + abs(from_col - den_col)
            new_dist = abs(to_row - den_row) + abs(to_col - den_col)
            if new_dist < cur_dist: score += (cur_dist - new_dist) * 5 
            scored_moves.append((move, score))
        #sort by score in descending order, highest first
        scored_moves.sort(key=lambda x: x[1], reverse=True)
        return [move for move, _ in scored_moves]
    def alpha_beta(self, board, depth, alpha, beta, current_player, player):
        winner = is_game_over(board)
        if winner: return 1000 if winner == current_player else -1000
        #check if position was evaluated before
        board_hash = self.hash_board(board)
        if board_hash in self.memory_box and self.memory_box[board_hash]['depth'] >= depth: return self.memory_box[board_hash]['score']
        #base case for recursive
        if depth == 0:
            score = self.evaluate_board(board, current_player)
            self.memory_box[board_hash] = {'score': score, 'depth': 0}
            return score
        valid_moves = self.get_all_valid_moves(board, current_player)
        if not valid_moves: return -1000    #no valid moves = loss
        valid_moves = self.order_moves(valid_moves, board, current_player, player)
        best_score = float('-inf')
        next_player = 'green' if current_player == 'red' else 'red'
        for move in valid_moves:
            new_board = self.make_temp_move(board, move)
            #call recursively alpha beta cut
            score = -self.alpha_beta(new_board, depth-1, -beta, -alpha, next_player, player+1)
            #update score and alpha
            if score > best_score: best_score, best_move = score, move
            alpha = max(alpha, score)
            #alpha-beta
            if alpha >= beta:
                #add to killer moves if not a capture
                to_row, to_col = move[1]
                if board[to_row][to_col] is None and move not in self.killer_moves.get(player, []):
                    if len(self.killer_moves.get(player, [])) >= 2: self.killer_moves[player].pop(0)  #eemove oldest
                    if player not in self.killer_moves: self.killer_moves[player] = []
                    self.killer_moves[player].append(move)
                break
        #store in memory box for future reference
        self.memory_box[board_hash] = {'score': best_score, 'depth': depth}
        return best_score
    
    def hash_board(self, board):
        board_str = ""
        for row in range(9):
            for col in range(7):
                piece = board[row][col]
                #piece exists, ad info
                if piece: board_str += f"{row}{col}{piece.color}{piece.type}"
                #add '_' if not
                else: board_str += f"{row}{col}__"
        return board_str
