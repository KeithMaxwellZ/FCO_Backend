import json

from flask import Flask, request
from main import Engine
from utils import EngineException
import actions

app = Flask(__name__)


class EngineManager:
    def __init__(self):
        self.expert_engine = {}
        self.c = 0

    def init(self):
        uid = self.c
        self.expert_engine[uid] = None
        self.c += 1
        return uid

    def start(self, userid,
              progEff, qltyEff, cpTotal,
              duraTotal, progTotal, qltyTotal, progDiff, qltyDiff, progLvl, qltyLvl, statusMode=2):
        self.expert_engine[userid] = Engine(progEff, qltyEff, cpTotal,
                                            duraTotal, progTotal, qltyTotal, progDiff, qltyDiff, progLvl, qltyLvl,
                                            statusMode=2)

    def get_info(self, userid):
        e: Engine
        e = self.expert_engine[userid]
        payload = {
            "CurrentProgress": e.prog_current,
            "CurrentQuality": e.qlty_current,
            "CurrentCP": e.cp_current,
            "CurrentDurability": e.dura_current,
            "Buffs": e.buffs
        }
        return json.dumps(payload)

    def use_action(self, userid, action_id):
        r = self.expert_engine[userid].use_action(actions.ACTIONS_ALL[action_id])
        return r


def payload_gen(code, msg, data):
    return json.dumps({
        "code": code,
        "message": msg,
        "data": data
    })


@app.route('/actions', methods=['GET'])
def get_skills():
    return payload_gen(200, "Success", {"ActionList": actions.ACTION_ID})


@app.route('/initiate', methods=['GET'])
def initiate():
    uid = em.init()
    return payload_gen(200, "Success", uid)


@app.route('/engine/<int:uid>/<cmd>', methods=['POST'])
def engine(uid: int, cmd):
    data = json.loads(request.data)
    if cmd == "start":
        try:
            em.start(
                uid,
                progEff=data['ProgressEfficiency'],
                qltyEff=data['QualityEfficiency'],
                cpTotal=data['TotalCP'],
                duraTotal=data['TotalDurability'],
                progTotal=data['TotalProgress'],
                qltyTotal=data['TotalQuality'],
                progDiff=data['ProgressDifficulty'],
                qltyDiff=data['QualityDifficulty'],
                progLvl=data['ProgressLevel'],
                qltyLvl=data['QualityLevel'],
                statusMode=data['Mode']
            )
            return payload_gen(200, 'Success', None)
        except KeyError as e:
            return payload_gen(1, "Missing Key", {"Missing": e.args[0]})
    elif cmd == "use-action":
        try:
            r = em.use_action(uid, data['Action'])
            return payload_gen(200, 'Success', {"Action Result": r})
        except KeyError:
            return payload_gen(1, "Missing Action", None)
    else:
        pass


@app.route('/engine/<int:uid>', methods=['GET'])
def info(uid):
    return payload_gen(200, "Success", em.get_info(uid))


if __name__ == '__main__':
    em = EngineManager()
    app.run()
