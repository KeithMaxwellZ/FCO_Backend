import math
import random


class Status:
    def __init__(self, name, color, rate):
        """
        class for crafting status
        :param name: name of the status
        :param color: corresponding color
        """
        self.name = name
        self.color = color
        self.rate = rate


WHITE = Status("normal", "white", -1)
RED = Status("HQ", "red", 12)
YELLOW = Status("Centered", "yellow", 15)
CYAN = Status("Malleable", "cyan", 12)
BLUE = Status("Sturdy", "blue", 15)
PURPLE = Status("Primed", "purple", 12)
GREEN = Status("Pliant", "green", 12)
Orange = Status("GoodOmen", "Orange", 15)

BLACK = Status("Poor", "black", -1)
RAINBOW = Status("Excellent", "rainbow", -1)

STATUS_REF = {
    'white': WHITE,
    'red': RED,
    'yellow': YELLOW,
    'cyan': CYAN,
    'blue': BLUE,
    'purple': PURPLE,
    'green': GREEN,
    'good_omen': Orange,
}

ORDER = [Orange, CYAN, PURPLE, GREEN, BLUE, YELLOW, BLACK, RAINBOW, RED, WHITE]


class StatusManager:
    BASIC = 0
    NORMAL = 1
    HARD = 2
    NORMAL_STATUS = [WHITE, RED, BLACK, RAINBOW]
    HARD_STATUS = [RED, YELLOW, CYAN, BLUE, PURPLE]

    def __init__(self, mode=2):
        """
        :param mode: Crafting mode
        """
        self.last = WHITE
        self.mode = mode

        self.table = []

        if mode > 1:
            bin_arr = "{0:b}".format(mode).zfill(len(ORDER))
            for i in range(len(ORDER)):
                if bin_arr[i] == '1':
                    for j in range(ORDER[i].rate):
                        self.table.append(ORDER[i])
        while len(self.table) < 100:
            self.table.append(WHITE)

    def next_status(self):
        if self.mode == 0:
            return WHITE
        elif self.mode == 1:
            next_status = None
            if self.last == RAINBOW:
                next_status = BLACK
            elif random.randint(0, 100) < 4:
                next_status = RAINBOW
            elif random.randint(0, 100) < 20:
                # 20% for red
                next_status = RED
            else:
                next_status = WHITE
            self.last = next_status
            return next_status
        elif self.mode >= 2:
            if self.last == Orange:
                return RED
            r = random.randint(0, 99)
            return self.table[r]
