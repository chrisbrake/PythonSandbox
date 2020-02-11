import requests
import uwsgi
"""
uwsgi --module "microWsgi.websockets:application" --http :5050 --stats stats.socket 

curl -i -N \
     -H "Connection: Upgrade" \
     -H "Upgrade: websocket" \
     -H "Host: 127.0.0.1:5050" \
     -H "Origin: 127.0.0.1:5050" \
     127.0.0.1:5051

"""


def application(env, start_response):
    # complete the handshake
    uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
    while True:
        msg = uwsgi.websocket_recv()
        uwsgi.websocket_send(msg)
