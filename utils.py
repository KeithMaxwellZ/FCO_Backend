BUFF_TABLE = {
    "Muscle Memory": 0,
    "Observation": 1,
    "Waste Not": 2,
    "Manipulation": 3,
    "Veneration": 4,
    "Great Stride": 5,
    "Innovation": 6,
    "Final Appraisal": 7,
    "Heart and Soul": 8
}

BUFF_TABLE_REV = {
    0: "Muscle Memory",
    1: "Observation",
    2: "Waste Not",
    3: "Manipulation",
    4: "Veneration",
    5: "Great Stride",
    6: "Innovation",
    7: "Final Appraisal",
    8: "Heart and Soul"
}


class EngineException(Exception):
    def __init__(self, msg, errid):
        self.msg = msg
        self.errid = errid
