import json

from flask import Flask, request
from main import Engine
from utils import EngineException

app = Flask(__name__)

engine = None

@app.route('/get')
def hello_world():
    print("Received")
    return 'Hello World'


@app.route('/post', methods=['POST'])
def post_test():
    print(request)
    print(request.data)
    r = json.loads(request.data)
    print(r)
    return "0"


if __name__ == '__main__':
    app.run()
