# calculates the score for particular rolling effect
from random import randrange

class Item:

    def __init__(self):
        self.dice = [0]*5
        self.rollAll()

    def values(self):
        return list(self.dice)

    def roll(self, which):
        for pos in which:
            self.dice[pos] = randrange(1,6,1)

    def rollAll(self):
        self.roll(range(5))

    def score(self):
        counts = [0] * 7
        for value in self.dice:
            counts[value] = counts[value] + 1
        if 5 in counts:
            return "You have Five of a Kind", 30
        elif 4 in counts:
            return "You have Four of a Kind", 15
        elif (3 in counts) and (2 in counts):
            return "You have Full House", 12
        elif (not (3 in counts)) and (not (2 in counts)) \
             and (counts[1]==0):
            return "You have Big Straight", 25
        elif (not (3 in counts)) and (not (2 in counts)) \
             and (counts[6]==0):
            return "You have Small Straight", 20
        elif 3 in counts:
            return "You have Three of a Kind", 8
        elif counts.count(2) == 2:
            return "You have Two Pairs", 5
        elif 2 in counts:
            return "You have a pair", 1
        else:
            return "Garbage", -20
        



