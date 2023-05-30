from requests import get
from flask import jsonify, make_response


def make_req(url: str):
    try: 
        res = get(url)

        return not str(res.status_code).startswith('4')
    except: 
        return False


def networking_handler():
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