import json
from bottle import run, route, post, request

ephemeral_db = list()


@route('/')
def return_all():
    return ephemeral_db


@post('/')
def append():
    ephemeral_db.append(json.load(request.body))


if __name__ == '__main__':
    run(host='0.0.0.0')
