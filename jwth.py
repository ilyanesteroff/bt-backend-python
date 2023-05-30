import jwt
from os import urandom
from flask import jsonify, make_response


def jwt_handler(): 
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