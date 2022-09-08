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
GREEN = Status("忘了", "green")


class StatusManager:
    BASIC = 0
    NORMAL = 1
    HARD = 2
    NORMAL_STATUS = [WHITE, RED]
    HARD_STATUS = [WHITE, RED, YELLOW, CYAN, BLUE, PURPLE]

    def __init__(self, mode=2):
        """

        :param mode: Crafting mode
        """
        self.mode = mode

    def next_status(self):
        if self.mode == 0:
            return WHITE
        elif self.mode == 1:
            # 20% for red
            if random.randint(0, 100) > 20:
                return WHITE
            else:
                return RED
        elif self.mode == 2:
            # Evenly distributed TODO: need some data
            r = math.floor(random.random() * len(StatusManager.HARD_STATUS))
            return StatusManager.HARD_STATUS[r]

