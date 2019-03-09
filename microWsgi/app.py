import logging
import falcon

"""
uwsgi --module "microWsgi.app:assemble()" --http :5050

curl -s http://localhost:5050 | python -m 'json.tool'
"""
logging.basicConfig(level=logging.DEBUG)


def ready(req, resp):
    return {"status": "ready"}


def params(req, resp):
    return req.params


class Tester(object):

    tests = {
        'ready': ready,
        'params': params,
    }

    def on_get(self, req, resp, resource):
        if resource:
            logging.debug('resource: %s', resource)
            resp.media = self.tests[resource](req, resp)
        else:
            resp.media = {k: v(req, resp) for k, v in self.tests.items()}
            resp.media['test'] = 'potato'
            logging.debug('data: %s', resp.data)
            logging.debug('media: %s', resp.media)
        logging.debug('params: %s', req.params)


def assemble():
    app = falcon.API()
    app.add_route('/{resource}', Tester())
    return app
