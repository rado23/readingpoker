# play.py

# main module which starts the game and instruction panel
# The Reading Poker has been created by Yelena Matros, Andreas Savvides and Radoslaw Rozkowinski
# This game has been developed using our knowledge from our Python lectures
# and tutorials initially, and from Books and on-line guides
# such as the one available at python.org
# Some of the most helpful and significant books that we have used to help
# us develop this game were:
# Python Scripting for Computational Science - Hans Petter Langtangen
# Core Python Programming - Wesley J. Chun
# Python 2.1 Bible - Dave Brueck and Stephen Tanner
# Python, how to program - Deitel
# Python Programming for the Absolute Beginner - Michael Dawson
# The instructions for how to use this game and play it are displayed below
# as they will be as soon as the game is loaded.


from drawing import *
from bu_maker import BMaker
from clrview import CShowDice

class DrawMaker:

    def __init__(self):
        self.win = GraphWin("Reading Poker Instruction", 800, 600) # starts instruction window
        self.win.setBackground("yellow")
        banner = Text(Point(400,30), "Welcome to the Reading Poker!")
        banner.setSize(28)
        banner.setFill("blue")
        banner.setStyle("bold")
        banner.draw(self.win)
        self.msg = Text(Point(400,80), "Welcome to the game!")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,100), "You play Poker using 5 dice. You have 150 credits on the beginning.")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,120), "Each game costs you 15 credits. After first rolling dice you have")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,140), "two more chances to roll chosen dice again.")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,160), "Your goal is to earn as many credits as possible. You score as follow:")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,180), "A pair gives you 1 credit")
        self.msg.setSize(14)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg.draw(self.win)
        self.msg = Text(Point(400,200), "Two pairs give you 5 credits")
        self.msg.setSize(14)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg.draw(self.win)
        self.msg = Text(Point(400,220), "Three of a kind give you 8 credits")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg = Text(Point(400,240), "Full house give you 12 credits")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg = Text(Point(400,260), "Four of a kind give you 15 credits")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg = Text(Point(400,280), "Small straight give you 20 credits")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg = Text(Point(400,300), "Big straight give you 25 credits")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg = Text(Point(400,320), "Five of a kind (POKER) give you 30 credits")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg.setFill ("red")
        self.msg.setStyle ("bold")
        self.msg = Text(Point(400,340), "If you do not have any of above after three rollings,")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,360), "it costs you 20 credits. Your scores cumulate continuously.")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,380), "Game terminates when you have no credits to pay for next turns.")
        self.msg.setSize(14)
        self.msg.draw(self.win)
        self.msg = Text(Point(400,500), "ENJOY THE GAME!")
        self.msg.setSize(26)
        self.msg.draw(self.win)
        self.msg.setFill ("red3")
        self.msg.setStyle ("bold")
                     
        self.win = GraphWin("Reading Poker", 600, 400) # starts the game window
        self.win.setBackground("green3")
        banner = Text(Point(300,30), "Reading Poker")
        banner.setSize(24)
        banner.setFill("yellow2")
        banner.setStyle("bold")
        banner.draw(self.win)
        self.msg = Text(Point(300,380), "Welcome to the game!")
        self.msg.setSize(18)
        self.msg.draw(self.win)
        self.createDice(Point(300,100), 75)
        self.buttons = []
        self.addDiceButtons(Point(300,170), 75, 30)
        b = BMaker(self.win, Point(300, 230), 400, 40, "Roll Dice")
        self.buttons.append(b)
        b = BMaker(self.win, Point(300, 280), 150, 40, "Score")
        self.buttons.append(b)
        b = BMaker(self.win, Point(570,375), 40, 30, "Quit")
        self.buttons.append(b)
        self.money = Text(Point(300,325), "credits: 150")
        self.money.setSize(18)
        self.money.draw(self.win)
        
    def createDice(self, center, size): # places dice in the game window
        center.move(-3*size,0)
        self.dice = []
        for i in range(5):
            view = CShowDice(self.win, center, size)
            self.dice.append(view)
            center.move(1.5*size,0)

    def addDiceButtons(self, center, width, height): # places buttons which should be pushed to chose die to be rolled
        center.move(-3*width, 0)
        for i in range(1,6):
            label = "Die %d" % (i)
            b = BMaker(self.win, center, width, height, label)
            self.buttons.append(b)
            center.move(1.5*width, 0)

    def choose(self, choices): # makes particular buttons 'active' or 'inactive'
        buttons = self.buttons
        for b in buttons:
            if b.getLabel() in choices:
                b.activate()
            else:
                b.deactivate()
        while 1:
            p = self.win.getMouse()
            for b in buttons:
                if b.clicked(p):
                    return b.getLabel()

    def setMoney(self, amt): # shows credits 
        self.money.setText("credits: %d" % (amt))

    def setDice(self, values): # sets dice value
        for i in range(5):
            self.dice[i].setValue(values[i])

    def wantToPlay(self): # activates menu whether you want to play or finish the game
        ans = self.choose(["Roll Dice", "Quit"])
        self.msg.setText("")
        return ans == "Roll Dice"

    def close(self): # closes the game
        self.win.close()

    def showResult(self, msg, score): # shows results
        if score > 0:
            text = "%s! You win credits: %d" % (msg, score)
        else:
            text = "You rolled %s" % (msg)
        self.msg.setText(text)

    def chooseDice(self): # selects which dice to roll
        choices = []
        while 1:
            b = self.choose(["Die 1", "Die 2", "Die 3", "Die 4", "Die 5",
                             "Roll Dice", "Score"])
            if b[0] == "D":
                i = eval(b[4]) - 1
                if i in choices:
                    choices.remove(i)
                    self.dice[i].setColor("black")
                else:
                    choices.append(i)
                    self.dice[i].setColor("gray")
            else:
                for d in self.dice:
                    d.setColor("black")
                if b == "Score":
                    return []
                elif choices != []:
                    return choices
    

from readingp import ReadingPoker

inter = DrawMaker()
app = ReadingPoker(inter)
app.run()


