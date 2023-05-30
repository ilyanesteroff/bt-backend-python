from json import load, dumps
from datetime import datetime
from random import getrandbits
from flask import jsonify, make_response


FILENAME = './file.json'


def read_file(filename):
    with open(filename, "r") as f:
        return load(f)


def write_file(filename, data):
    with open(filename, "w") as f:
        f.write(data)


def fs_handler(): 
    json_data = read_file(FILENAME)

    key = getrandbits(32).to_bytes(4, "big").hex()

    value = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    json_data[key] = value

    write_file(f"./tmp/{key}.json", dumps(json_data))

    response = make_response(jsonify(**json_data), 201)
    
    return response