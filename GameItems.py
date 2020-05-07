class Cash():
    def __init__(self, value):
        self.value = value
        self.itemDescription = "You got $" + str(self.value) + "!";
        self.itemName = "$" + str(self.value)
        
        if self.value == 5000:
            self.numCash = 1
        elif self.value == 3000:
            self.numCash = 2
        elif self.value == 1000:
            self.numCash = 10
        elif self.value == 200:
            self.numCash = 24
        else: #this should never be triggered.
            self.numCash = 0
    
class Rob():
    def __init__(self):
        self.itemDescription = "You robbed someone!"
        self.itemName = "Rob"

class Bank():
    def __init__(self):
        self.itemDescription = "Your cash is safe in the bank!"
        self.itemName = "Bank"

class ChooseNextSquare():
    def __init__(self):
        self.itemDescription = "You can choose the next square!"
        self.itemName = "ChooseNextSquare"
    
class Present():
    def __init__(self):
        self.itemDescription = "You gave someone a present!"
        self.itemName = "Present"

class Mirror():
    def __init__(self):
        self.itemDescription = "You got a mirror!"
        self.itemName = "Mirror"

class Shield():
    def __init__(self):
        self.itemDescription = "You got a shield!"
        self.itemName = "Shield"

class Backstab():
    def __init__(self):
        self.itemDescription = "You back stabbed someone!"
        self.itemName = "Backstab"

class LostAtSea():
    def __init__(self):
        self.itemDescription = "You got lost at sea!"
        self.itemName = "LostAtSea"

class DoubleScore():
    def __init__(self):
        self.itemDescription = "You doubled your score!"
        self.itemName = "DoubleScore"

class SinkShip():
    def __init__(self):
        self.itemDescription = "You sank someone's ship!"
        self.itemName = "SinkShip"

class SneakPeak():
    def __init__(self):
        self.itemDescription = "You sneak peeked someone!"
        self.itemName = "SneakPeek"

class SwapScore():
    def __init__(self):
        self.itemDescription = "You swapped scores!"
        self.itemName = "SwapScore"