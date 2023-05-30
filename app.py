import os
from flask import Flask
from fs import fs_handler
from jwth import jwt_handler
from networking import networking_handler
from benchmarking import stop_measuring, start_measuring


app = Flask(__name__)


@app.route('/measure/start', methods=['POST'])
def measureStart():
    return start_measuring()


@app.route('/measure/stop', methods=['POST'])
def measureStop():
    return stop_measuring()


@app.route('/jwt', methods=['POST'])
def jwt_token(): 
    return jwt_handler()


@app.route('/fs', methods=['POST'])
def fs(): 
    return fs_handler()


@app.route('/networking', methods=['POST'])
def networking():
    return networking_handler()


if __name__ == '__main__':
    app.run(debug=True, port=os.environ.get('PORT') or 5000)
