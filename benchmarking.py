import psutil 
from math import ceil
from os import getpid
from flask import jsonify, make_response


STATS = {
  "CPU": None,
  "MEM": None
}


def start_measuring():
    process = psutil.Process(getpid())
    memory = process.memory_info()
    cpu_time = (process.cpu_times().user + process.cpu_times().system) * 1e6 / psutil.cpu_count()

    STATS["CPU"] = cpu_time

    STATS["MEM"] = memory.rss

    response = make_response(jsonify(key="OK"), 201)
    
    return response


def stop_measuring():
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