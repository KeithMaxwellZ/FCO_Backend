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
        "ERROR：已完成制作",
        "ERROR：当前非首回合，无法使用该技能",
        "ERROR：非“高品质”状态，无法使用该技能",
        "ERROR：“内静”不足10层，无法使用该技能",
        "ERROR：制作力不足，无法使用该技能",
        "ERROR：在本次制作中已经使用过该技能，无法再次使用",
        "ERROR：无法在“俭约”状态下使用该技能"
    ]

    def __init__(self, errid):
        self.msg = EngineException.EXCEPTIONS[errid]
        self.errid = errid
