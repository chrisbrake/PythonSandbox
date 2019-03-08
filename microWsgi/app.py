import falcon

"""
uwsgi --module "microWsgi.app:assemble()" --http :5050

curl -s http://localhost:5050 | python -m 'json.tool'
"""


def ready(req, resp):
    return {"ready": "yes"}


class Tester(object):

    tests = {
        'ready': ready,
    }

    def on_get(self, req, resp, resource):
        if resource:
            resp.media = self.tests[resource](req, resp)
        resp.media = {k: v(req, resp) for k, v in self.tests.items()}


def assemble():
    app = falcon.API()
    app.add_route('/{resource}', Tester())
    return app
