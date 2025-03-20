# player.py
class Player:
    """
    Classe para representar um jogador no jogo Animal Chess.
    """

    def __init__(self, name, color):
        """
        Inicializa o jogador com seu nome e cor.
        """
        self.name = name
        self.color = color

    def get_move(self, board):
        """
        Obtém a jogada do jogador.
        (Por enquanto, apenas retorna None, pois a entrada será tratada diretamente no game.py)
        """
        return None

    def is_valid_move(self, board, start_pos, end_pos):
        """
        Verifica se o movimento é válido para este jogador.
        (Por enquanto, a lógica de validação está no board.py)
        """
        # A lógica de validação de movimento será implementada no board.py
        return board.is_valid_move(self, start_pos[0], start_pos[1], end_pos[0], end_pos[1])