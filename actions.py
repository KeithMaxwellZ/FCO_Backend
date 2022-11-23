import status

from utils import *

ACTION_ID = {}
ACTIONS_ALL = []


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
        self.name = name
        self.durability_cost = durability_cost
        self.cp_cost = cp_cost
        self.success_rate = success_rate
        self.progress_multiplier = progress_multiplier
        self.quality_multiplier = quality_multiplier
        self.buff = buff

        ACTION_ID[self.name] = len(ACTIONS_ALL)
        ACTIONS_ALL.append(self)

    def check_success(self, engine):
        """
        Check if the condition is met
        :param engine: current engine instance
        :return: success rate
        """
        return self.success_rate

    def __str__(self):
        return self.name


class MuscleMemory(ActionBase):
    def __init__(self):
        super().__init__("Muscle Memory", 10, 6, 1.0, 3.0, 0.0, 5)

    def check_success(self, engine):
        if engine.turn > 0:
            raise EngineException(1)
        return self.success_rate


class Reflect(ActionBase):
    def __init__(self):
        super().__init__("Reflect", 10, 6, 1.0, 0.0, 1.0, -1)

    def check_success(self, engine):
        if engine.turn > 0:
            raise EngineException(1)
        return self.success_rate


# Synthesis actions
class BasicSynth(ActionBase):
    def __init__(self):
        super().__init__("Basic Synth", 10, 0, 1.0, 1.2, 0.0, -1)


class CarefulSynth(ActionBase):
    def __init__(self):
        super().__init__("Careful Synth", 10, 7, 1.0, 1.8, 0.0, -1)


class RapidSynth(ActionBase):
    def __init__(self):
        super().__init__("Rapid Synth", 10, 0, 0.5, 5.0, 0.0, -1)


class FocusedSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Focused Synth", 10, 5, 0.5, 2.0, 0.0, -1)

    def check_success(self, engine):
        return self.success_rate + (0.5 if engine.buffs[1] > 0 else 0)


class Groundwork(ActionBase):
    def __init__(self):
        super().__init__("Groundwork", 20, 18, 1.0, 3.6, 0.0, -1)


class IntensiveSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Intensive Synthesis", 10, 6, 1.0, 4.0, 0.0, -1)

    def check_success(self, engine):
        if engine.status != status.RED:
            if engine.buffs[8] > 0:
                engine.buffs[8] = 0
            else:
                raise EngineException(2)
        return self.success_rate


class PrudentSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Prudent Synthesis", 5, 18, 1.0, 1.8, 0.0, -1)

    def check_success(self, engine):
        if engine.buffs[2] > 0:
            raise EngineException(6)
        return self.success_rate


class DelicateSynthesis(ActionBase):
    def __init__(self):
        super().__init__("Delicate Synthesis", 10, 32, 1.0, 1.0, 1.0, -1)


# Touch actions
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
        super().__init__("Byregots Blessing", 10, 24, 1.0, 0.0, 1.0, -1)


class PreciseTouch(ActionBase):
    def __init__(self):
        super().__init__("Precise Touch", 10, 18, 1.0, 0.0, 1.5, -1)

    def check_success(self, engine):
        if engine.status != status.RED:
            if engine.buffs[8] > 0:
                engine.buffs[8] = 0
            else:
                raise EngineException(2)
        return self.success_rate


class PrudentTouch(ActionBase):
    def __init__(self):
        super().__init__("Prudent Touch", 5, 25, 1.0, 0.0, 1.0, -1)

    def check_success(self, engine):
        if engine.buffs[2] > 0:
            raise EngineException(6)
        return self.success_rate


class FocusedTouch(ActionBase):
    def __init__(self):
        super().__init__("Focused Touch", 10, 18, 0.5, 0.0, 1.5, -1)

    def check_success(self, engine):
        return self.success_rate + (0.5 if engine.buffs[1] > 0 else 0)


class PreparatoryTouch(ActionBase):
    def __init__(self):
        super().__init__("Preparatory Touch", 20, 40, 1.0, 0.0, 2.0, -1)


class AdvancedTouch(ActionBase):
    def __init__(self):
        super().__init__("Advanced Touch", 10, 46, 1.0, 0.0, 1.5, -1)


class TrainedFinesse(ActionBase):
    def __init__(self):
        super().__init__("Trained Finesse", 0, 32, 1.0, 0.0, 1.25, -1)

    def check_success(self, engine):
        if engine.inner_quiet < 10:
            raise EngineException(3)
        return self.success_rate


class MastersMend(ActionBase):
    def __init__(self):
        super().__init__("Master's Mend", 0, 88, 1.0, 0.0, 0.0, -1)

    def check_success(self, engine):
        engine.dura_current = min((engine.dura_current + 30), engine.dura_total)
        return self.success_rate


class WasteNot(ActionBase):
    def __init__(self):
        super().__init__("Waste Not", 0, 58, 1.0, 0.0, 0.0, 24)


class WasteNotII(ActionBase):
    def __init__(self):
        super().__init__("Waste Not II", 0, 98, 1.0, 0.0, 0.0, 28)


class Manipulation(ActionBase):
    def __init__(self):
        super().__init__("Manipulation", 0, 96, 1.0, 0.0, 0.0, 38)

    def check_success(self, engine):
        engine.buffs[3] = 0
        return self.success_rate


class Veneration(ActionBase):
    def __init__(self):
        super().__init__("Veneration", 0, 18, 1.0, 0.0, 0.0, 44)


class GreatStrides(ActionBase):
    def __init__(self):
        super().__init__("Great Strides", 0, 32, 1.0, 0.0, 0.0, 53)


class Innovation(ActionBase):
    def __init__(self):
        super().__init__("Innovation", 0, 18, 1.0, 0.0, 0.0, 64)


class Observe(ActionBase):
    def __init__(self):
        super().__init__("Observe", 0, 7, 1.0, 0.0, 0.0, 11)


class TricksOfTheTrade(ActionBase):
    def __init__(self):
        super().__init__("Tricks of the Trade", 0, 0, 1.0, 0.0, 0.0, -1)

    def check_success(self, engine):
        if engine.status != status.RED:
            raise EngineException(2)
        engine.cp_current = min(engine.cp_current + 20, engine.cp_total)
        return self.success_rate


class FinalAppraisal(ActionBase):
    def __init__(self):
        super().__init__("Final Appraisal", 0, 1, 1.0, 0.0, 0.0, -1)

    def check_success(self, engine):
        # if engine.faReady <= 0:
        #     raise EngineException(5)
        # engine.faReady -= 1
        engine.cp_current -= 1
        engine.buffs[7] = 5
        return 0


class HeartAndSoul(ActionBase):
    def __init__(self):
        super().__init__("Heart And Soul", 0, 0, 1.0, 0.0, 0.0, -1)

    def check_success(self, engine):
        if engine.hsReady <= 0:
            raise EngineException(5)
        engine.hsReady -= 1
        engine.buffs[8] = 999
        return 0


class CarefulObservation(ActionBase):
    def __init__(self):
        super().__init__("Careful Observation", 0, 0, 1.0, 0.0, 0.0, -1)

    def check_success(self, engine):
        if engine.caReady <= 0:
            raise EngineException(5)
        engine.caReady -= 1
        engine.status = engine.status_manager.next_status()
        return 0


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

if __name__ == '__main__':
    print(ACTIONS_ALL)
    for i in ACTIONS_ALL:
        print(i)
