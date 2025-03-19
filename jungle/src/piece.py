import os 



class Piece:
    def __init__(self,name,color,value,can_jump=False,can_swim=False,eat_rat=True,eat_elephant=False,texture=None,texture_rect=None):
        self.name=name
        self.color=color
        value_sign=1 if color=='green' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.set_texture()
        self.texture_rect = texture_rect

        def set_texture(self,size=360):
            self.texture=os.path.join(
                f'assets/images/imgs/{self.color}_{self.name}.png'
            )

        def add_moves(self,move):
            self.moves.append(move)

class Den(Piece):
    def __init__(self, color):
        super().__init__('den', color, 0)  # valor 0 pois não se move

class Trap(Piece):
    def __init__(self, color):
        super().__init__('trap', color, 0)  # valor 0 pois não se move

class Rat(Piece):
    def __init__(self, color):
        super().__init__('rat', color, 1.0, can_swim=True, eat_elephant=True)

class Cat(Piece):
    def __init__(self, color):
        super().__init__('cat', color, 2.0)

class Dog(Piece):
    def __init__(self, color):
        super().__init__('dog', color, 3.0)

class Wolf(Piece):
    def __init__(self, color):
        super().__init__('wolf', color, 4.0)

class Leopard(Piece):
    def __init__(self, color):
        super().__init__('leopard', color, 5.0)
    
class Tiger(Piece):
    def __init__(self, color):
        super().__init__('tiger', color, 6.0, can_jump=True)

class Lion(Piece):
    def __init__(self, color):
        super().__init__('lion', color, 7.0, can_jump=True)

class Elephant(Piece):
    def __init__(self, color):
        super().__init__('elephant', color, 8.0, eat_rat=False)



