ACTION_TABLE = {}


class ActionBase:
    def __init__(
            self,
            name: str = "",
            durability_cost: int = 0,
            cp_cost: int = 0,
            success_rate: float = 1.0,
            progress_multiplier: float = 0.0,
            quality_multiplier: float = 0.0,
            buff=-1
    ):
        self.id = len(ACTION_TABLE)

        self.name = name
        self.durability_cost = durability_cost
        self.cp_cost = cp_cost
        self.success_rate = success_rate
        self.progress_multiplier = progress_multiplier
        self.quality_multiplier = quality_multiplier
        self.buff = buff

        ACTION_TABLE[self.name] = self

    def check_success(self, engine):
        return True


class MuscleMemory(ActionBase):
    def __init__(self):
        super().__init__("Muscle Memory", 0, 6, 1.0, 0.0, 3.0, -1)


class Reflect(ActionBase):
    def __init__(self):
        super().__init__("Reflect", 0, 6, 1.0, 1.0, 0.0, -1)


class BasicSynth(ActionBase):
    def __init__(self):
        super().__init__("Basic Synth", 10, 0, 1.0, 1.2, 0.0, -1)


class CarefulSynth(ActionBase):
    def __init__(self):
        super().__init__("Careful Synth", 10, 7, 1.0, 1.8, 0.0, -1)


class RapidSynth(ActionBase):
    def __init__(self):
        super().__init__("Rapid Synth", 10, 0, 0.5, 2.5, 0.0, -1)


class FocusedSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Focused Synth", 10, 5, 0.5, 2.0, 0.0, -1)


class Groundwork(ActionBase):
    def __init__(self):
        super().__init__("Groundwork", 20, 18, 1.0, 3.6, 0.0, -1)


class IntensiveSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Intensive Synthesis", 10, 6, 1.0, 4.0, 0.0, -1)


class PrudentSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Prudent Synthesis", 5, 18, 1.0, 1.8, 0.0, -1)


class DelicateSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Groundwork", 10, 32, 1.0, 1.0, 1.0, -1)


class BasicTouch(ActionBase):
    def __init__(self):
        super().__init__("Basic Touch", 10, 18, 1.0, 0.0, 1.0, -1)


class HastyTouch(ActionBase):
    def __init__(self):
        super().__init__("Hasty Touch", 10, 0, 0.6, 0.0, 1.0, -1)


class StandardTouch(ActionBase):
    def __init__(self):
        super().__init__("Standard Touch", 10, 32, 1.0, 0.0, 1.25, -1)


class ByregotsBlessing(ActionBase):
    def __init__(self):
        super().__init__("Byregots Touch", 10, 32, 1.0, 0.0, 1.25, -1)


class PreciseTouch(ActionBase):
    def __init__(self):
        super().__init__("Precise Touch", 10, 18, 1.0, 0.0, 1.5, -1)


class PrudentTouch(ActionBase):
    def __init__(self):
        super().__init__("Prudent Touch", 5, 25, 1.0, 0.0, 1.0, -1)


class FocusedTouch(ActionBase):
    def __init__(self):
        super().__init__("Focused Touch", 10, 18, 0.5, 0.0, 1.5, -1)


class PreparatoryTouch(ActionBase):
    def __init__(self):
        super().__init__("Preparatory Touch", 20, 40, 1.0, 0.0, 2.0, -1)


class AdvancedTouch(ActionBase):
    def __init__(self):
        super().__init__("Advanced Touch", 10, 46, 1.0, 0.0, 1.5, -1)


class TrainedFinesse(ActionBase):
    def __init__(self):
        super().__init__("Trained Finesse", 10, 32, 1.0, 0.0, 1.25, -1)


class MastersMend(ActionBase):
    def __init__(self):
        super().__init__("Master's Mend", 0, 88, 1.0, 0.0, 0.0, -1)


class WasteNot(ActionBase):
    def __init__(self):
        super().__init__("Waste Not", 0, 58, 1.0, 0.0, 0.0, -1)


class WasteNotII(ActionBase):
    def __init__(self):
        super().__init__("Waste Not II", 0, 98, 1.0, 0.0, 0.0, -1)


class Manipulation(ActionBase):
    def __init__(self):
        super().__init__("Waste Not", 0, 96, 1.0, 0.0, 0.0, -1)


class Veneration(ActionBase):
    def __init__(self):
        super().__init__("Veneration", 0, 18, 1.0, 0.0, 0.0, -1)


class GreatStrides(ActionBase):
    def __init__(self):
        super().__init__("Great Strides", 0, 32, 1.0, 0.0, 0.0, -1)


class Innovation(ActionBase):
    def __init__(self):
        super().__init__("Innovation", 0, 18, 1.0, 0.0, 0.0, -1)


class Observe(ActionBase):
    def __init__(self):
        super().__init__("Observe", 0, 7, 1.0, 0.0, 0.0, -1)


class TricksOfTheTrade(ActionBase):
    def __init__(self):
        super().__init__("Tricks of the Trade", 0, 0, 1.0, 0.0, 0.0, -1)


class FinalAppraisal(ActionBase):
    def __init__(self):
        super().__init__("Final Appraisal", 0, 1, 1.0, 0.0, 0.0, -1)


class HeartAndSoul(ActionBase):
    def __init__(self):
        super().__init__("HeartAndSoul", 0, 0, 1.0, 0.0, 0.0, -1)


MuscleMemory = MuscleMemory()
Reflect = Reflect()
BasicSynth = BasicSynth()
CarefulSynth = CarefulSynth()
RapidSynth = RapidSynth()
FocusedSynthesis = FocusedSynthesis()
Groundwork = Groundwork()
IntensiveSynthesis = IntensiveSynthesis()
PrudentSynthesis = PrudentSynthesis()
DelicateSynthesis = DelicateSynthesis()
BasicTouch = BasicTouch()
HastyTouch = HastyTouch()
StandardTouch = StandardTouch()
ByregotsBlessing = ByregotsBlessing()
PreciseTouch = PreciseTouch()
PrudentTouch = PrudentTouch()
FocusedTouch = FocusedTouch()
PreparatoryTouch = PreparatoryTouch()
AdvancedTouch = AdvancedTouch()
TrainedFinesse = TrainedFinesse()
MastersMend = MastersMend()
WasteNot = WasteNot()
WasteNotII = WasteNotII()
Manipulation = Manipulation()
Veneration = Veneration()
GreatStrides = GreatStrides()
Innovation = Innovation()
Observe = Observe()
TricksOfTheTrade = TricksOfTheTrade()
FinalAppraisal = FinalAppraisal()
HeartAndSoul = HeartAndSoul()
