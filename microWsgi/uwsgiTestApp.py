import json
import logging
import socket
import falcon
from . import db

"""
Server:
uwsgi --module "microWsgi.uwsgiTestApp:assemble()" --http :5050 --stats stats.socket 

Client:
curl -s 'http://localhost:5050?test=potatoes' | python -m 'json.tool'

Stats:
nc -U stats.socket | python -m 'json.tool'
"""
logging.basicConfig(level=logging.DEBUG)


def ready(req, resp):
    """ Proof of life """
    return {"ready": "yes"}


def params(req, resp):
    """ Params from the URL string """
    return req.params


def stats(req, resp):
    """ uwsgi's stats """
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect('./stats.socket')

    diag = b''
    part = b''
    while part or not diag:
        diag += part
        part = sock.recv(16)
    return json.loads(diag)


class Tester(object):
    """ Sandbox """

    tests = {
        'db': db.diag,
        'stats': stats,
        'params': params,
        'ready': ready,
    }

    def on_get(self, req, resp, resource):
        if resource:
            resp.media = self.tests[resource](req, resp)
        else:
            resp.media = {k: v(req, resp) for k, v in self.tests.items()}


def assemble():
    app = falcon.API()
    app.add_route('/{resource}', Tester())
    return app
