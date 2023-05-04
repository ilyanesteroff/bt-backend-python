import jwt
import psutil 
from math import ceil
from requests import get
from json import load, dumps
from datetime import datetime
from random import getrandbits
from os import urandom, getpid
from hashlib import pbkdf2_hmac, sha256
from flask import Flask, jsonify, make_response


app = Flask(__name__)


FILENAME = './file.json'


def make_req(url: str):
    try: 
        res = get(url)

        return not str(res.status_code).startswith('4')
    except: 
        return False
    
    
def read_file(filename):
    with open(filename, "r") as f:
        return load(f)


def write_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)



STATS = {
  "CPU": None,
  "MEM": None
}


@app.route('/measure/start', methods=['POST'])
def startMeasuring():
    process = psutil.Process(getpid())
    memory = process.memory_info()
    cpu_time = (process.cpu_times().user + process.cpu_times().system) * 1e6 / psutil.cpu_count()

    STATS["CPU"] = cpu_time

    STATS["MEM"] = memory.rss

    response = make_response(jsonify(key="OK"), 201)
    
    return response


@app.route('/measure/stop', methods=['POST'])
def stopMeasuring():
    process = psutil.Process(getpid())
    memory = process.memory_info()
    cpu_time = (process.cpu_times().user + process.cpu_times().system) * 1e6 / psutil.cpu_count()

    data = {
        "cpu": ceil(cpu_time) - ceil(STATS['CPU']),
        "mem": ((memory.rss - STATS["MEM"]) / (1024 * 1024))
    }

    STATS["CPU"] = None

    STATS["MEM"] = None

    response = make_response(jsonify(**data), 201)
    
    return response


@app.route('/jwt', methods=['POST'])
def jwt_token(): 
    username = urandom(8).hex().encode("utf-8").hex()
    secret = urandom(24).hex().encode("utf-8").hex()
    email = urandom(10).hex().encode("utf-8").hex()

    payload = {
        "username": username,
        "email": email
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    
    decoded = jwt.decode(token, secret, algorithms=["HS256"])

    response = make_response(jsonify(token=token, payload=decoded), 201)
    
    return response


@app.route('/crypto', methods=['POST'])
def crypto(): 
    password = urandom(8).hex().encode("utf-8")
 
    salt = 'salt'.encode("utf-8")
  
    key = pbkdf2_hmac("sha256", password, salt, 20000, 24).hex()

    hash = sha256(key.encode('utf-8')).hexdigest()

    response = make_response(jsonify(hash=hash, key=key), 201)
    
    return response


@app.route('/fs', methods=['POST'])
def fs(): 
    json_data = read_file(FILENAME)

    key = getrandbits(32).to_bytes(4, "big").hex()

    value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    json_data[key] = value

    write_file(f"./tmp/{key}.json", dumps(json_data))

    response = make_response(jsonify(**json_data), 201)
    
    return response


@app.route('/networking', methods=['POST'])
def networking():
    urls = [
      'https://www.google.com/',
      'https://www.airbnb.com/',
      'https://www.deel.com/'
    ]

    successfull = 0
    failed = 0

    for url in urls:
        res = make_req(url)

        if res: 
            successfull += 1
        else:   
            failed += 1

    status_code = 201

    response = make_response(jsonify(successfull=successfull, failed=failed), status_code)
    
    return response


if __name__ == '__main__':
    app.run(debug=True)
