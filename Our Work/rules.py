# rules.py
class Rules:
    """
    Classe para conter as regras do jogo Animal Chess.
    """

    @staticmethod
    def is_valid_move(board, piece, start_row, start_col, end_row, end_col):
        """
        Verifica se o movimento da peça é válido, considerando as regras do jogo.
        """
        # Regras gerais:

        # 1. Dentro dos limites do tabuleiro
        if not (0 <= end_row < board.height and 0 <= end_col < board.width):
            return False

        # 2. Não pode mover para a própria toca
        if (piece.color == "red" and end_row == 6 and end_col == 3) or \
           (piece.color == "blue" and end_row == 0 and end_col == 3):
            return False

        # 3. Não pode capturar peças da mesma cor
        target_piece = board.get_piece(end_row, end_col)
        if target_piece and target_piece.color == piece.color:
            return False

        # 4. Movimento de apenas uma casa (geralmente)
        if abs(start_row - end_row) + abs(start_col - end_col) != 1:
            # Verificar se é um pulo do Leão ou Tigre
            if piece.name in ("Lion", "Tiger"):
                if not Rules.can_jump_river(board, piece, start_row, start_col, end_row, end_col):
                    return False
            else:
                return False

        # Regras específicas de cada peça:

        # Rato:
        if piece.name == "Rat":
            # Pode entrar no rio
            if (end_row == 1 or end_row == 2 or end_row == 4 or end_row == 5) and \
               (end_col == 3 or end_col == 4 or end_col == 5):
                pass # Movimento válido para o rio
            #TODO: implementar a captura do Elefante pelo Rato

        # Leão e Tigre:
        if piece.name in ("Lion", "Tiger"):
            # Podem pular o rio
            pass # A verificação do pulo é feita acima
            #TODO: implementar o pulo sobre o rio

        # Regras de armadilhas:
        if (end_row == 0 and (end_col == 2 or end_col == 4)) or \
           (end_row == 1 and end_col == 3) or \
           (end_row == 5 and end_col == 3) or \
           (end_row == 6 and (end_col == 2 or end_col == 4)):
            #TODO: implementar a lógica da armadilha
            pass # Na armadilha, a força do animal é reduzida a 0

        # Regras de captura:
        if target_piece:
            if not piece.can_capture(target_piece):
                return False

        return True

    @staticmethod
    def can_jump_river(board, piece, start_row, start_col, end_row, end_col):
        """
        Verifica se a peça pode pular o rio.
        """
        # Só Leão e Tigre podem pular o rio
        if piece.name not in ("Lion", "Tiger"):
            return False

        # Pulo horizontal
        if start_row == end_row:
            # Pulo para a direita
            if end_col > start_col:
                for col in range(start_col + 1, end_col):
                    if not ((start_row == 1 or start_row == 5) and (col == 3 or col == 4 or col == 5)):
                        return False # Não está no rio
                    if board.get_piece(start_row, col) is not None:
                        return False # Tem uma peça no caminho
            # Pulo para a esquerda
            else:
                for col in range(end_col + 1, start_col):
                    if not ((start_row == 1 or start_row == 5) and (col == 3 or col == 4 or col == 5)):
                        return False # Não está no rio
                    if board.get_piece(start_row, col) is not None:
                        return False # Tem uma peça no caminho

        # Pulo vertical
        elif start_col == end_col:
            # Pulo para baixo
            if end_row > start_row:
                for row in range(start_row + 1, end_row):
                    if not ((start_col == 3 or start_col == 4 or start_col == 5) and (row == 1 or row == 2)):
                        return False # Não está no rio
                    if board.get_piece(row, start_col) is not None:
                        return False # Tem uma peça no caminho
            # Pulo para cima
            else:
                for row in range(end_row + 1, start_row):
                    if not ((start_col == 3 or start_col == 4 or start_col == 5) and (row == 1 or row == 2)):
                        return False # Não está no rio
                    if board.get_piece(row, start_col) is not None:
                        return False # Tem uma peça no caminho
        else:
            return False # Não é um pulo reto

        return True

    @staticmethod
    def is_game_over(board):
        """
        Verifica se o jogo terminou (um jogador alcançou a toca do oponente ou capturou todas as peças).
        """
        #TODO: implementar a lógica para verificar se o jogo terminou
        return False