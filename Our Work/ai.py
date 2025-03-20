# ai.py
import random
from player import Player
from rules import Rules

class AIPlayer(Player):
    """
    Classe para representar um jogador controlado por IA.
    """

    def __init__(self, name, color, depth=2):
        """
        Inicializa o jogador de IA com seu nome, cor e profundidade de busca.
        """
        super().__init__(name, color)
        self.depth = depth  # Profundidade da busca Minimax

    def get_move(self, board):
        """
        Obtém a melhor jogada para o jogador de IA usando o algoritmo Minimax.
        """
        best_move = None
        best_value = float('-inf')  # Inicializa com o menor valor possível
        alpha = float('-inf')
        beta = float('inf')

        for move in self.get_possible_moves(board):
            new_board = board.copy()  # Cria uma cópia do tabuleiro
            self.apply_move(new_board, move)  # Aplica o movimento ao tabuleiro de teste
            move_value = self.minimax(new_board, self.depth - 1, False, alpha, beta)  # Chama o Minimax para avaliar o movimento

            if move_value > best_value:
                best_value = move_value
                best_move = move

            alpha = max(alpha, best_value)  # Atualiza o valor de alpha

        return best_move  # Retorna o melhor movimento encontrado

    def minimax(self, board, depth, maximizing_player, alpha, beta):
        """
        Implementa o algoritmo Minimax com Alpha-Beta Pruning.
        """
        if depth == 0 or Rules.is_game_over(board):
            return self.evaluate_board(board)  # Avalia o tabuleiro

        if maximizing_player:
            max_value = float('-inf')
            for move in self.get_possible_moves(board):
                new_board = board.copy()
                self.apply_move(new_board, move)
                value = self.minimax(new_board, depth - 1, False, alpha, beta)
                max_value = max(max_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    break  # Beta cutoff
            return max_value
        else:
            min_value = float('inf')
            opponent_color = "red" if self.color == "blue" else "blue"
            for move in self.get_possible_moves(board, opponent_color):
                new_board = board.copy()
                self.apply_move(new_board, move)
                value = self.minimax(new_board, depth - 1, True, alpha, beta)
                min_value = min(min_value, value)
                beta = min(beta, value)
                if beta <= alpha:
                    break  # Alpha cutoff
            return min_value

    def get_possible_moves(self, board, color=None):
        """
        Retorna todos os movimentos possíveis para o jogador de IA.
        """
        if color is None:
            color = self.color
        moves = []
        for row in range(board.height):
            for col in range(board.width):
                piece = board.get_piece(row, col)
                if piece and piece.color == color:
                    # Para cada peça, verificar todos os movimentos possíveis
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if abs(dr) + abs(dc) == 1:  # Apenas movimentos adjacentes
                                new_row, new_col = row + dr, col + dc
                                if Rules.is_valid_move(board, piece, row, col, new_row, new_col):
                                    moves.append(((row, col), (new_row, new_col)))  # Adiciona o movimento como uma tupla de posições
        return moves

    def apply_move(self, board, move):
        """
        Aplica um movimento ao tabuleiro (usado para simulações).
        """
        start_row, start_col = move[0]
        end_row, end_col = move[1]
        piece = board.get_piece(start_row, start_col)
        board.move_piece(start_row, start_col, end_row, end_col)

    def evaluate_board(self, board):
        """
        Avalia o tabuleiro para determinar a "pontuação" de um estado.
        (Quanto maior a pontuação, melhor para o jogador de IA)
        """
        score = 0

        #TODO: melhorar a função de avaliação
        # Contar a diferença no número de peças
        red_pieces = 0
        blue_pieces = 0
        for row in range(board.height):
            for col in range(board.width):
                piece = board.get_piece(row, col)
                if piece:
                    if piece.color == "red":
                        red_pieces += piece.strength
                    else:
                        blue_pieces += piece.strength

        if self.color == "red":
            score = red_pieces - blue_pieces
        else:
            score = blue_pieces - red_pieces

        return score