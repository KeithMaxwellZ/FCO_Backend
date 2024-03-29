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
            duraTotal, progTotal, qltyTotal, progDiv, qltyDiv, progMod, qltyMod,
            red=1.5, statusMode=2):
        """
        check the comment for other args
        :param statusMode: see status.Status for available options
        """
        self.prog_eff = int(progEff)
        self.qlty_eff = int(qltyEff)
        self.cp_total = int(cpTotal)
        self.dura_total = int(duraTotal)
        self.prog_total = int(progTotal)
        self.qlty_total = int(qltyTotal)
        self.prog_div = int(progDiv) / 10
        self.qlty_div = int(qltyDiv) / 10
        self.prog_mod = int(progMod) / 100
        self.qlty_mod = int(qltyMod) / 100

        self.red = float(red)

        self.inner_quiet = 0  # Inner quiet level
        self.prog_current = 0  # Current progress
        self.qlty_current = 0  # Current quality
        self.cp_current = int(cpTotal)  # Current cp
        self.dura_current = int(duraTotal)  # Current durability
        self.turn = 0  # Current turn

        self.faReady = 1  # If Final Appraisal has been used
        self.hsReady = 1  # If Heart and Soul has been used
        self.caReady = 3

        self.touchCombo = 0

        self.finished = False  # If crafting is finished

        # Duration of buffs
        self.buffs = [0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.status = status.WHITE  # Current crafting status

        # Instance ofStatus Manager
        self.status_manager = status.StatusManager(int(statusMode))

    def use_action(self, action: ActionBase):
        # Check if crafting is finished
        if self.finished:
            raise EngineException(0)

        # Data for progress calculation (Maybe some improvements here)
        pim = action.progress_multiplier
        qim = action.quality_multiplier
        dc = action.durability_cost
        cc = action.get_cp(self)
        sr = action.check_success(self)
        create_buff = action.buff

        curr_status = self.status

        # Some specifications
        if action == actions.ByregotsBlessing:
            qim += 0.2 * self.inner_quiet

        if action == actions.Groundwork and self.dura_current - self.calculate_durability(dc) < 0:
            pim = pim / 2

        if sr == 0:
            # Continue without progressing turn count
            return 100

        # Calculations
        r = self.main_proc(
            pim, qim, dc, cc, sr, create_buff
        )

        # Specifications (reflect provides extra inner quiet
        if r == 100:
            if action == actions.MastersMend:
                print(111)
                self.dura_current = min((self.dura_current + 30), self.dura_total)
            if action == actions.ByregotsBlessing:
                self.inner_quiet = 0

            elif action == actions.Reflect:
                self.inner_quiet += 1

            elif action == actions.PreciseTouch:
                self.inner_quiet += 1

            elif action == actions.PreparatoryTouch:
                self.inner_quiet += 1

            if action == actions.BasicTouch:
                self.touchCombo = 1
            elif action == actions.StandardTouch and self.touchCombo == 1:
                self.touchCombo = 2
            else:
                self.touchCombo = 0

        if self.inner_quiet > 10:
            self.inner_quiet = 10

        return r

    def main_proc(self, prog_multiplier, qlty_multiplier, durability_cost, cp_cost, success_rate, create_buff):
        # Increase turn counter
        self.turn += 1

        # Some data setup
        prog_res = 0
        qlty_res = 0
        dura_res = self.calculate_durability(durability_cost)
        cp_res = self.calculate_cp(cp_cost)

        # Check if action is successful
        success = True
        if success_rate < 1:
            success_rate += (0.25 if self.status == status.YELLOW else 0)
            roll = random.randrange(0, 100, step=1) / 100
            success = (roll <= success_rate)
            # print(roll, success)

        # Calculate progress and quality increment if success
        if success:
            if prog_multiplier > 0:
                prog_res = self.calculate_prog(prog_multiplier)
                self.prog_current += prog_res
                self.prog_current = min(self.prog_current, self.prog_total)

                # Check final Appraisal
                if self.prog_current >= self.prog_total and self.buffs[7] > 0:
                    self.prog_current = self.prog_total - 1
                    self.buffs[7] = 0
            if qlty_multiplier > 0:
                qlty_res = self.calculate_qlty(qlty_multiplier)
                self.qlty_current += qlty_res
                self.qlty_current = min(self.qlty_current, self.qlty_total)
            print(self.prog_current, self.buffs)

        # Modify current data

        self.cp_current -= cp_res
        self.dura_current -= dura_res

        # Check finish conditions
        r = self.finish_check()

        if r == 100:  # Continue
            # Manipulation
            if self.buffs[3] > 0:
                self.dura_current = min(self.dura_current + 5, self.dura_total)

            # Buff countdown
            for i in range(0, len(self.buffs)):
                if self.buffs[i] > 0:
                    self.buffs[i] -= 1

            # Create buff if necessary
            if create_buff != -1:
                b = math.floor(create_buff / 10)
                d = create_buff - b * 10
                self.buffs[b] = d + (2 if (self.status == status.PURPLE and b != 1) else 0)

            # Generate next status
            self.status = self.status_manager.next_status()

        if not success:
            r += 1
        return r

    # 从桶老师帖子里毛来的（）
    def calculate_prog(self, prog_multiplier, predict=False):
        # 作业进展=rounddown(基准进展(base)*效率系数(efficiency)*作业状态系数(status_const),0)
        # 基准进展=rounddown(作业压制系数(progLvl)*(作业精度(progEff)/作业难度系数(progDiff)+2),0)
        base = self.prog_mod * (self.prog_eff / self.prog_div + 2)
        base = math.floor(base)
        buff = (1 if self.buffs[0] > 0 else 0) + (0.5 if self.buffs[4] > 0 else 0)
        if not predict:
            self.buffs[0] = 0
        status_const = 1.5 if self.status == status.CYAN else 1
        efficiency = prog_multiplier * (1 + buff)
        return math.floor(base * efficiency * status_const)

    # 也是从桶老师帖子里毛来的（）
    def calculate_qlty(self, qlty_multiplier, predict=False):
        # 加工品质=rounddown(基准品质(base)*效率系数(efficiency)*内静系数(inner_quiet_efficiency)*品质状态系数(status_const),0)
        # 基准品质=rounddown(加工压制系数(qltyLvl)*(加工精度(qltyEff)/加工难度系数(qltyDiff)+35),0)
        base = self.qlty_mod * (self.qlty_eff / self.qlty_div + 35)
        base = math.floor(base)
        buff = (1 if self.buffs[5] > 0 else 0) + (0.5 if self.buffs[6] > 0 else 0)
        if not predict:
            self.buffs[5] = 0
        status_const = self.red if self.status == status.RED else 1
        efficiency = qlty_multiplier * (1 + buff)
        inner_quiet_efficiency = 1 + 0.1 * self.inner_quiet
        if not predict:
            self.inner_quiet += 1
        return math.floor(base * efficiency * inner_quiet_efficiency * status_const)

    def calculate_durability(self, durability_cost):
        return math.floor(
            durability_cost *  # Base durability cost
            (0.5 if self.buffs[2] > 0 else 1) *  # Efficiency from buff
            (0.5 if self.status == status.BLUE else 1) +  # Efficiency from status
            0.5  # Modification for rounding
        )

    def calculate_cp(self, cp_cost):
        if cp_cost * (0.5 if self.status == status.GREEN else 1) > self.cp_current:
            raise EngineException(4)
        return math.floor(
            cp_cost *  # Base cp cost
            (0.5 if self.status == status.GREEN else 1) +  # Efficiency from status
            0.5  # Modification for rounding
        )

    def finish_check(self):
        if self.prog_current >= self.prog_total:
            # Success
            self.finished = True
            return 200
        if self.dura_current <= 0:
            # Fail
            self.finished = True
            return -1
        # Continue
        return 100

    def gen_buffs(self):
        data = {}
        for i in range(len(self.buffs)):
            data[BUFF_TABLE_REV[i]] = self.buffs[i]
        return data

    def save_data(self):
        payload = {
            "prog_eff": self.prog_eff,
            "qlty_eff": self.qlty_eff,
            "cp_total": self.cp_total,
            "dura_total": self.dura_total,
            "prog_total": self.prog_total,
            "qlty_total": self.qlty_total,
            "prog_div": self.prog_div,
            "qlty_div": self.qlty_div,
            "prog_mod": self.prog_mod,
            "qlty_mod": self.qlty_mod,
            "inner_quiet": self.inner_quiet,
            "prog_current": self.prog_current,
            "qlty_current": self.qlty_current,
            "cp_current": self.cp_current,
            "dura_current": self.dura_current,
            "turn": self.turn,
            "hsReady": self.hsReady,
            "caReady": self.caReady,
            "finished": self.finished,
            "buffs": self.buffs,
            "status": self.status.color,
            "status_mode": self.status_manager.mode
        }

        return payload

    def load_data(self, payload):
        self.prog_eff = int(payload['prog_eff'])
        self.qlty_eff = int(payload['qlty_eff'])
        self.cp_total = int(payload['cp_total'])
        self.dura_total = int(payload['dura_total'])
        self.prog_total = int(payload['prog_total'])
        self.qlty_total = int(payload['qlty_total'])
        self.prog_div = int(payload['prog_div'])
        self.qlty_div = int(payload['qlty_div'])
        self.prog_mod = int(payload['prog_mod'])
        self.qlty_mod = int(payload['qlty_mod'])

        self.inner_quiet = int(payload['inner_quiet'])
        self.prog_current = int(payload['prog_current'])
        self.qlty_current = int(payload['qlty_current'])
        self.cp_current = int(payload['cp_current'])
        self.dura_current = int(payload['dura_current'])
        self.turn = int(payload['turn'])

        self.hsReady = int(payload['hsReady'])
        self.caReady = int(payload['caReady'])

        self.finished = payload['finished']

        self.buffs = payload['buffs']

        self.status = status.STATUS_REF[payload['status']]

        self.status_manager = status.StatusManager(int(payload['status_mode']))

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

    def predict(self, action: ActionBase):
        prog_multiplier = action.progress_multiplier
        qlty_multiplier = action.quality_multiplier
        dc = action.durability_cost
        cc = action.cp_cost
        sr = action.check_success(self)
        create_buff = action.buff

        # Some specifications
        if action == actions.ByregotsBlessing:
            qlty_multiplier += 0.2 * self.inner_quiet

        if action == actions.Groundwork and self.dura_current - self.calculate_durability(dc) < 0:
            pim = prog_multiplier / 2

        if sr == 0:
            # Continue without progressing turn count
            return 100

        prog_res = 0
        qlty_res = 0

        if prog_multiplier > 0:
            prog_res = self.calculate_prog(prog_multiplier, predict=True)
        if qlty_multiplier > 0:
            qlty_res = self.calculate_qlty(qlty_multiplier, predict=True)

        return prog_res, qlty_res


if __name__ == '__main__':
    e = Engine(
        2552, 2662, 605, 80,
        3000, 25565, 13, 11.5, 1, 1,
        statusMode=0
    )
    e.use_action(actions.MuscleMemory)
    e.use_action(actions.Veneration)
    e.dbg()
    e.use_action(actions.BasicSynth)
    e.dbg()
    e.use_action(actions.FinalAppraisal)
    e.dbg()
    e.use_action(actions.Groundwork)
