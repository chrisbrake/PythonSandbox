import multiprocessing
import gunicorn.app.base


def main(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return environ.items()


class WebApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(WebApplication, self).__init__()

    def load_config(self):
        for key, value in self.options:
            self.cfg.set(key, value)

    def load(self):
        return self.application


if __name__ == '__main__':
    config = [
        ('bind', '%s:%s' % ('127.0.0.1', '8080')),
        ('workers', multiprocessing.cpu_count()),
    ]

    WebApplication(main, config).run()
