# the module responsible for dice poker application
from do_dice import Item

class ReadingPoker:

    def __init__(self, interface):
        self.dice = Item()
        self.money = 150
        self.interface = interface

    def run(self): # runs the game if you have enough credits 
        while self.money >= 15 and self.interface.wantToPlay():
            self.playRound()            
        self.interface.close()

    def playRound(self): # a turn
        self.money = self.money - 15
        self.interface.setMoney(self.money)
        self.doRolls()
        result, score = self.dice.score()
        self.interface.showResult(result, score)
        self.money = self.money + score
        self.interface.setMoney(self.money)        

    def doRolls(self): # rolling dices (no more than 3 times)
        self.dice.rollAll()
        roll = 1
        self.interface.setDice(self.dice.values())
        toRoll = self.interface.chooseDice()
        while roll < 3 and toRoll != []:
            self.dice.roll(toRoll)
            roll = roll + 1
            self.interface.setDice(self.dice.values())
            if roll < 3:
                toRoll = self.interface.chooseDice()


