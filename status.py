import math
import random


class Status:
    def __init__(self, name, color):
        """
        class for crafting status
        :param name: name of the status
        :param color: corresponding color
        """
        self.name = name
        self.color = color


WHITE = Status("normal", "white")
RED = Status("HQ", "red")
YELLOW = Status("Centered", "yellow")
CYAN = Status("Malleable", "cyan")
BLUE = Status("Sturdy", "blue")
PURPLE = Status("Primed", "purple")
GREEN = Status("Pliant", "green")

BLACK = Status("Poor", "black")
RAINBOW = Status("Excellent", "rainbow")


class StatusManager:
    BASIC = 0
    NORMAL = 1
    HARD = 2
    NORMAL_STATUS = [WHITE, RED, BLACK, RAINBOW]
    HARD_STATUS = [WHITE, RED, YELLOW, CYAN, BLUE, PURPLE]

    def __init__(self, mode=2):
        """

        :param mode: Crafting mode
        """
        self.last = WHITE
        self.mode = mode

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
        elif self.mode == 2:
            # Evenly distributed TODO: need some data
            r = math.floor(random.random() * len(StatusManager.HARD_STATUS))
            self.last = StatusManager.HARD_STATUS[r]
            return self.last

