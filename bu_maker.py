from drawing import Rectangle, Text, Point

class BMaker:

    def __init__(self, win, center, width, height, label):
        # Creates a button

        w, h = width / 2.0, height / 2.0
        x, y = center.getX(), center.getY()
        self.xmax, self.xmin = x + w, x - w
        self.ymax, self.ymin = y + h, y - h

        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)

        self.rect = Rectangle(p1, p2)
        self.rect.setFill('pink')
        self.rect.draw(win)

        self.label = Text(center, label)
        self.label.draw(win)

        self.deactivate()

    def clicked(self, p):
        # Returns true if the button is active and p is inside
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def get_label(self):
        # Returns the label string of the button.
        return self.label.getText()

    def activate(self):
        # Makes the button look active
        self.label.setFill('blue3')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        # Makes the button look inactive
        self.label.setFill('pink3')
        self.rect.setWidth(1)
        self.active = 0
