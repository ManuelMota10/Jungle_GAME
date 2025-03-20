# cli.py
from main import Game

class CLI:
    """
    Classe para implementar a interface de linha de comando do jogo.
    """

    def __init__(self):
        """
        Inicializa o jogo e a interface de linha de comando.
        """
        self.game = Game()

    def display_board(self):
        """
        Exibe o tabuleiro no terminal.
        """
        #TODO: implementar a lógica para exibir o tabuleiro em formato de texto
        pass

    def get_player_move(self, player):
        """
        Obtém a jogada do jogador a partir da entrada do usuário.
        """
        #TODO: implementar a lógica para obter a jogada do jogador
        pass

    def run(self):
        """
        Executa o loop principal do jogo na linha de comando.
        """
        while not self.game.is_game_over():
            self.display_board()
            move = self.get_player_move(self.game.current_player)
            self.game.make_move(move)
            self.game.switch_player()

        print("Fim de jogo!")