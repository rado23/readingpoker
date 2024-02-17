# play.py


from drawing import *
from bu_maker import BMaker
from clrview import CShowDice

class DrawMaker:

    def __init__(self):
        self.create_instruction_window()
        self.create_game_window()

    def create_instruction_window(self):
        instruction_win = GraphWin("Reading Poker Instruction", 800, 600)
        instruction_win.setBackground("yellow")
        self.create_banner(instruction_win)
        self.create_instruction_messages(instruction_win)

    def create_banner(self, win):
        banner = Text(Point(400, 30), "Welcome to the Reading Poker!")
        banner.setSize(28)
        banner.setFill("blue")
        banner.setStyle("bold")
        banner.draw(win)

    def create_instruction_messages(self, win):
        messages = [
            "Welcome to the game!",
            "You play Poker using 5 dice. You have 150 credits on the beginning.",
            "Each game costs you 15 credits. After first rolling dice you have",
            "two more chances to roll chosen dice again.",
            "Your goal is to earn as many credits as possible. You score as follow:",
            "A pair gives you 1 credit",
            "Two pairs give you 5 credits",
            "Three of a kind give you 8 credits",
            "Full house give you 12 credits",
            "Four of a kind give you 15 credits",
            "Small straight give you 20 credits",
            "Big straight give you 25 credits",
            "Five of a kind (POKER) give you 30 credits",
            "If you do not have any of above after three rollings,",
            "it costs you 20 credits. Your scores cumulate continuously.",
            "Game terminates when you have no credits to pay for next turns.",
            "ENJOY THE GAME!"
        ]
        self.create_text_messages(win, messages)

    def create_text_messages(self, win, messages):
        y_position = 100
        for message in messages:
            text = Text(Point(400, y_position), message)
            text.setSize(14)
            if "credits" in message:
                text.setFill("red")
                text.setStyle("bold")
            text.draw(win)
            y_position += 20

    def create_game_window(self):
        game_win = GraphWin("Reading Poker", 600, 400)
        game_win.setBackground("green3")
        self.create_game_banner(game_win)
        self.create_game_elements(game_win)

    def create_game_banner(self, win):
        banner = Text(Point(300, 30), "Reading Poker")
        banner.setSize(24)
        banner.setFill("yellow2")
        banner.setStyle("bold")
        banner.draw(win)

    def create_game_elements(self, win):
        self.create_dice(win, Point(300, 100), 75)
        self.create_dice_buttons(win, Point(300, 170), 75, 30)
        self.create_buttons(win)

    def create_dice(self, win, center, size):
        center.move(-3 * size, 0)
        dice = [CShowDice(win, center, size) for _ in range(5)]

    def create_dice_buttons(self, win, center, width, height):
        center.move(-3 * width, 0)
        labels = ["Die 1", "Die 2", "Die 3", "Die 4", "Die 5"]
        buttons = [BMaker(win, center, width, height, label) for label in labels]

    def create_buttons(self, win):
        buttons = [
            BMaker(win, Point(300, 230), 400, 40, "Roll Dice"),
            BMaker(win, Point(300, 280), 150, 40, "Score"),
            BMaker(win, Point(570, 375), 40, 30, "Quit")
        ]

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
    

from readingp import ReadingPoker

inter = DrawMaker()
app = ReadingPoker(inter)
app.run()


