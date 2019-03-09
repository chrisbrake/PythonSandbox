import logging
import falcon
from . import db
"""
uwsgi --module "microWsgi.app:assemble()" --http :5050

curl -s 'http://localhost:5050?test=potatoes' | python -m 'json.tool'
"""
logging.basicConfig(level=logging.DEBUG)


def status(req, resp):
    """ Proof of life """
    return {"status": "ready"}


def params(req, resp):
    """ Params from the URL string """
    return req.params


class Tester(object):
    """ Sandbox """

    tests = {
        'db': db.diag,
        'params': params,
        'status': status,
    }

    def on_get(self, req, resp, resource):
        if resource:
            resp.media = self.tests[resource](req, resp)
        else:
            resp.media = {k: v(req, resp) for k, v in self.tests.items()}
        logging.debug('data: %s', resp.data)
        logging.debug('media: %s', resp.media)
        logging.debug('params: %s', req.params)
        logging.debug('resource: %s', resource)


def assemble():
    app = falcon.API()
    app.add_route('/{resource}', Tester())
    return app
