# piece.py
import pygame

class Piece:
   
    def __init__(self, name, color, strength):
        
        self.name = name
        self.color = color
        self.strength = strength
        self.image = pygame.image.load(f"assets/{self.color}_{self.name.lower()}.png") # Carrega a imagem da peça
        self.image = pygame.transform.scale(self.image, (80, 80)) # Redimensiona a imagem

    def can_capture(self, other_piece):
        
        if other_piece is None:
            return True  

        if self.color == other_piece.color:
            return False  

        if self.strength >= other_piece.strength:
            return True  
        else:
            return False

    def draw(self, screen, x, y):
        """
        Desenha a peça na tela.
        """
        screen.blit(self.image, (x, y))

class Elephant(Piece):
    def __init__(self, color):
        super().__init__("Elephant", color, 8)

    def can_capture(self, other_piece):
        
        if other_piece.name == "Rat" and other_piece.color != self.color:
            return False 
        return super().can_capture(other_piece)

class Lion(Piece):
    def __init__(self, color):
        super().__init__("Lion", color, 7)

class Tiger(Piece):
    def __init__(self, color):
        super().__init__("Tiger", color, 6)

class Panther(Piece):
    def __init__(self, color):
        super().__init__("Panther", color, 5)

class Dog(Piece):
    def __init__(self, color):
        super().__init__("Dog", color, 4)

class Wolf(Piece):
    def __init__(self, color):
        super().__init__("Wolf", color, 3)

class Cat(Piece):
    def __init__(self, color):
        super().__init__("Cat", color, 2)

class Rat(Piece):
    def __init__(self, color):
        super().__init__("Rat", color, 1)

    def can_capture(self, other_piece):
        
        if other_piece.name == "Elephant" and other_piece.color != self.color:
            return True  # Rato pode capturar o elefante
        return super().can_capture(other_piece)