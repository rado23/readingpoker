# changes colours of dice
from dielook import ShowDice

class CShowDice(ShowDice):

    def setValue(self, value):
        self.value = value      
        ShowDice.setValue(self, value) 

    def setColor(self, color):
        self.foreground = color
        self.setValue(self.value)

