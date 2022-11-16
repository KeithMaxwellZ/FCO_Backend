BUFF_TABLE = {
    "Muscle Memory": 0,
    "Observer": 1,
    "Waste Not": 2,
    "Manipulation": 3,
    "Veneration": 4,
    "Great Strides": 5,
    "Innovation": 6,
    "Final Appraisal": 7,
    "Heart And Soul": 8
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
    8: "Heart And Soul"
}


class EngineException(Exception):
    EXCEPTIONS = [
        "Finished",
        "Not 1st turn",
        "Not HQ",
        "Inner Quiet < 10",
        "No enough CP",
        "Already Used"
    ]

    def __init__(self, errid):
        self.msg = EngineException.EXCEPTIONS[errid]
        self.errid = errid
