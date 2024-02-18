from drawing import Rectangle, Point, Circle
import math

PIP_COLORS = ["black", "red", "green", "blue", "magenta", "cyan", "yellow"]


class DiceFace:

    def __init__(self, value):
        self.value = value

    def draw(self, canvas, center, size, outline, fill):
        # Draw dice rectangle
        offset = size / 2 * 0.6
        p1 = Point(center.x - size / 2, center.y - size / 2)
        p2 = Point(center.x + size / 2, center.y + size / 2)
        rect = Rectangle(p1, p2)
        rect.draw(canvas)
        rect.setWidth(2)
        rect.setOutline(outline)
        rect.setFill(fill)

        # Draw pips
        self.pips = generate_pips(self.value)
        for x, y in self.pips:
            pip = Circle(Point(center.x + x * offset, center.y + y * offset), size * 0.1)
            pip.draw(canvas)
            pip.setOutline(outline)
            pip.setFill(fill)

    def set_pip_color(self, canvas, color):
        for x, y in self.pips:
            pip = Circle(Point(self.center.x + x * self.offset, self.center.y + y * self.offset), self.size * 0.1)
            pip.setFill(color)


def generate_pips(value):
    pip_coords = []

    # Handle each dice value:
    if value == 1:
        pip_coords.append((0, 0))

    elif value == 2:
        pip_coords.append((-1, -1))
        pip_coords.append((1, 1))

    elif value == 3:
        pip_coords.append((-1, -1))
        pip_coords.append((0, 0))
        pip_coords.append((1, 1))

    elif value == 4:
        pip_coords.append((-1, -1))
        pip_coords.append((1, -1))
        pip_coords.append((-1, 1))
        pip_coords.append((1, 1))

    elif value == 5:
        pip_coords.append((-1, -1))
        pip_coords.append((1, -1))
        pip_coords.append((0, 0))
        pip_coords.append((-1, 1))
        pip_coords.append((1, 1))

    elif value == 6:
        pip_coords.append((-1, -1))
        pip_coords.append((1, -1))
        pip_coords.append((-1, 0))
        pip_coords.append((1, 0))
        pip_coords.append((-1, 1))
        pip_coords.append((1, 1))

    return pip_coords


class ShowDice:

    def __init__(self, canvas, center, size):
        self.canvas = canvas
        self.center = center
        self.size = size
        self.faces = dict()

    def set_value(self, value):
        if value not in self.faces:
            self.faces[value] = DiceFace(value)
        self.faces[value].draw(self.canvas, self.center, self.size, "black", "white")


class CShowDice(ShowDice):

    def set_color(self, color):
        self.faces[self.value].set_pip_color(self.canvas, color)
