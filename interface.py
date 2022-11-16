import json

from flask import Flask, request

import status
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
              duraTotal, progTotal, qltyTotal, progDiv, qltyDiv, progMod, qltyMod, statusMode=2):
        self.expert_engine[userid] = Engine(progEff, qltyEff, cpTotal,
                                            duraTotal, progTotal, qltyTotal, progDiv, qltyDiv, progMod, qltyMod,
                                            statusMode=2)

    def get_info(self, userid):
        e: Engine
        e = self.expert_engine[userid]
        payload = {
            "CurrentProgress": e.prog_current,
            "CurrentQuality": e.qlty_current,
            "CurrentCP": e.cp_current,
            "CurrentDurability": e.dura_current,
            "CurrentStatus": e.status.name,
            "Buffs": e.gen_buffs(),
            "InnerQuiet": e.inner_quiet,
        }
        print(payload)
        return payload

    def use_action(self, userid, action_id):
        r = self.expert_engine[userid].use_action(actions.ACTIONS_ALL[action_id])
        return r


em = EngineManager()


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
    return payload_gen(200, "Success", {"uid": uid})


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
                progDiv=data['ProgressDivider'],
                qltyDiv=data['QualityDivider'],
                progMod=data['ProgressModifier'],
                qltyMod=data['QualityModifier'],
                statusMode=data['Mode']
            )
            return payload_gen(200, 'Success', None)
        except KeyError as e:
            return payload_gen(301, "Missing Key", {"Missing": e.args[0]})
    elif cmd == "use-action":
        try:
            r = em.use_action(uid, data['Action'])
            return payload_gen(200, 'Success', {"Action Result": r})
        except KeyError:
            return payload_gen(302, "Missing Action", None)
        except EngineException as e:
            return payload_gen(310 + e.errid, EngineException.EXCEPTIONS[e.errid], None)
    else:
        # TODO: add exception
        pass


@app.route('/engine/<int:uid>', methods=['GET'])
def info(uid):
    print('aaa', uid)
    r = payload_gen(200, "Success", em.get_info(uid))
    print('bbb', r)
    return r


if __name__ == '__main__':
    app.run(host="0.0.0.0")
