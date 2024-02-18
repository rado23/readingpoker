from random import randrange


class Item:

    def __init__(self):
        self.dice = [0] * 5
        self.roll_all()
        self.counts = None
        self.hand = None

    def values(self):
        return self.dice

    def roll(self, which):
        for pos in which:
            self.dice[pos] = randrange(1, 7)
        self.counts = None
        self.hand = None

    def roll_all(self):
        self.roll(range(5))
        self.counts = None
        self.hand = None

    def score(self):
        if self.counts is None:
            self.counts = {value: 0 for value in range(1, 7)}
            for value in self.dice:
                self.counts[value] += 1

        if self.hand is None:
            if 5 in self.counts.values():
                self.hand = ("Five of a Kind", 30)
            elif 4 in self.counts.values():
                self.hand = ("Four of a Kind", 15)
            # ...rest of scoring logic
            elif 3 in self.counts and 2 in self.counts:
                return "You have Full House", 12
            elif 0 not in self.counts[1:6] and self.counts[6] == 0:
                return "You have Big Straight", 25
            elif self.counts[1] == 0 and 0 not in self.counts[2:7]:
                return "You have Small Straight", 20
            elif 3 in self.counts:
                return "You have Three of a Kind", 8
            elif self.counts.count(2) == 2:
                return "You have Two Pairs", 5
            elif 2 in self.counts:
                return "You have a pair", 1
            else:
                return "Garbage", -20

        return self.hand
