class animal:
    def __init__(self,name,streght,position,player,can_swim=False,can_jump=False):
        self.name=name
        self.streght=streght
        self.position=position
        self.player=player
        self.can_swim=can_swim
        self.can_jump=can_jump
    def move(self,new_position):
        self.position=new_position
class rat(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Rat', 1, position, player, can_swim=True)
class cat(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Cat', 2, position, player)
class dog(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Dog', 3, position, player)
class wolf(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Wolf', 4, position, player)
class leopard(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Leopard', 5, position, player)
class tiger(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Tiger', 6, position, player, can_jump=True)
class lion(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Lion', 7, position, player, can_jump=True)
class elephant(animal):
    def __init__(self, name, streght, position, player):
        super().__init__('Elephant', 6, position, player)
