import math
import random

import actions
import status
from actions import ActionBase
from utils import *



class Engine:
    """
    作业进展=rounddown(基准进展*效率系数,0)
    基准进展=rounddown(作业压制系数(progLvl)*(作业精度(progEff)/作业难度系数(progDiff)+2),0)
    加工品质=rounddown(基准品质*效率系数*内静系数*品质状态系数,0)
    基准品质=rounddown(加工压制系数(qltyLvl)*(加工精度(qltyEff)/加工难度系数(qltyDiff)+35),0)
    https://nga.178.com/read.php?tid=31075581

    white: normal
    red: qlty * 2
    yellow: successRate*2
    cyan: prog * 2
    blue: dura / 2
    purple: buff + 2
    """
    def __init__(
            self,
            progEff, qltyEff, cpTotal,
            duraTotal, progTotal, qltyTotal, progDiff, qltyDiff, progLvl, qltyLvl,
            statusMode=2):
        self.prog_eff = progEff
        self.qlty_eff = qltyEff
        self.cp_total = cpTotal
        self.dura_total = duraTotal
        self.prog_total = progTotal
        self.qlty_total = qltyTotal
        self.prog_diff = progDiff
        self.qlty_diff = qltyDiff
        self.prog_lvl = progLvl
        self.qlty_lvl = qltyLvl

        # Just in case TODO: need further data
        self.prog_lvl = 0.8
        self.qlty_lvl = 0.7

        self.inner_quiet = 0
        self.prog_current = 0
        self.qlty_current = 0
        self.cp_current = cpTotal
        self.dura_current = duraTotal
        self.turn = 0

        self.faReady = True

        self.hsReady = True

        self.finished = False

        self.buffs = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.status = None
        self.status_manager = status.StatusManager(statusMode)

    def use_action(self, action: ActionBase):
        if self.finished:
            raise EngineException("Finished", -1)

        pim = action.progress_multiplier
        qim = action.quality_multiplier
        dc = action.durability_cost
        cc = action.cp_cost
        sr = action.check_success(self)
        create_buff = action.buff

        # TODO: Specifications
        pass
        if sr == 0:
            return 100
        r = self.main_proc(
            pim, qim, dc, cc, sr, create_buff
        )

        # TODO: refelct check

        return r

    def main_proc(self, prog_multiplier, qlty_multiplier, durability_cost, cp_cost, success_rate, create_buff):
        self.turn += 1

        prog_res = 0
        qlty_res = 0
        dura_res = self.calculate_durability(durability_cost)
        cp_res = self.calculate_cp(cp_cost)

        success = True
        if success_rate < 1:
            success_rate += 0.25 if self.status == status.YELLOW else 0
            success = random.randrange(0, 1) >= success_rate

        if success:
            if prog_multiplier > 0:
                prog_res = self.calculate_prog(prog_multiplier)
            if qlty_multiplier > 0:
                qlty_res = self.calculate_qlty(qlty_multiplier)

        self.prog_current += prog_res
        self.qlty_current += qlty_res
        self.cp_current -= cp_res
        self.dura_current -= dura_res

        if self.prog_current > self.prog_total and self.buffs[7] > 0:
            self.prog_current = self.prog_total - 1
            self.buffs[7] = 0

        r = self.finish_check()

        if r == 0:
            if self.buffs[3] > 0:
                self.dura_current = (self.dura_current + 5) % self.dura_total

            for i in range(0, len(self.buffs)):
                if self.buffs[i] > 0:
                    self.buffs[i] -= 1

            # TODO: Generate next status
            if create_buff != -1:
                b = math.floor(create_buff / 10)
                d = create_buff - b * 10
                self.buffs[b] = d + (2 if self.status == status.PURPLE and b != 1 else 0)

        return 0

    def calculate_prog(self, prog_multiplier):
        base = self.prog_lvl * (self.prog_eff / self.prog_diff + 2)
        base = math.floor(base)
        buff = (1 if self.buffs[0] > 0 else 0) + (0.5 if self.buffs[4] > 0 else 0)
        self.buffs[0] = 0
        status_const = 1.5 if self.status == status.CYAN else 1
        efficiency = prog_multiplier * (1 + buff)
        print(prog_multiplier, base, buff, efficiency, status_const, 1.2*3)
        return math.floor(base * efficiency * status_const)

    def calculate_qlty(self, qlty_multiplier):
        base = self.qlty_lvl * (self.qlty_eff / self.qlty_diff + 35)
        base = math.floor(base)
        buff = (1 if self.buffs[5] > 0 else 0) + (0.5 if self.buffs[6] > 0 else 0)
        self.buffs[5] = 0
        status_const = 1.5 if self.status == status.RED else 1
        efficiency = qlty_multiplier * (1 + buff)
        inner_quiet_efficiency = 1 + 0.1 * self.inner_quiet
        return math.floor(base * efficiency * inner_quiet_efficiency * status_const)

    def calculate_durability(self, durability_cost):
        return math.floor(
            durability_cost *
            (0.5 if self.buffs[2] > 0 else 1) *
            (0.5 if self.status == status.BLUE else 1) +
            0.5
        )

    def calculate_cp(self, cp_cost):
        return math.floor(cp_cost / (2 if self.status == status.GREEN else 1) + 0.5)

    def finish_check(self):
        if self.qlty_current >= self.qlty_total:
            self.finished = True
            return 1
        if self.dura_current <= 0:
            self.finished = True
            return -1
        return 0

    def dbg(self):
        print("Turn: " + str(self.turn))
        print(f"     Current | Total")
        print(f"Prog {str(self.prog_current).rjust(7)} | {str(self.prog_total).rjust(5)}")
        print(f"Qlty {str(self.qlty_current).rjust(7)} | {str(self.qlty_total).rjust(5)}")
        print(f"Dura {str(self.dura_current).rjust(7)} | {str(self.dura_total).rjust(5)}")
        for i in range(0, len(self.buffs)):
            if self.buffs[i] != 0:
                print(f"{BUFF_TABLE_REV[i]}: {self.buffs[i]}")
        print("=====================")


if __name__ == '__main__':
    e = Engine(
            2552, 2662, 605, 80,
            3000, 25565, 13, 11.5, 1, 1
        )
    e.use_action(ActionBase(buff=BUFF_TABLE["Veneration"] * 10 + 4))
    e.dbg()
    e.use_action(actions.BasicSynth)
    e.dbg()
    e.use_action(actions.BasicSynth)
    e.dbg()
