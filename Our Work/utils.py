# utils.py
def coordinates_to_position(col, row, square_size, offset_x, offset_y):
    """
    Converte coordenadas de linha e coluna do tabuleiro para posições (x, y) na tela.
    """
    x = col * square_size + offset_x
    y = row * square_size + offset_y
    return x, y

def position_to_coordinates(x, y, square_size, offset_x, offset_y):
    """
    Converte posições (x, y) na tela para coordenadas de linha e coluna do tabuleiro.
    """
    col = (x - offset_x) // square_size
    row = (y - offset_y) // square_size
    return col, row