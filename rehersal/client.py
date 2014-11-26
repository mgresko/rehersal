import json
import logging
import time

import zmq

from config import c

log = logging.getLogger(__name__)

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.connect(c.broker.sub_endpoint)

    for request in range(1,11):
        data = [
            'puppet',
            {'branch': 'TECHOPS-{0}'.format(request)}
        ]
        log.debug("Sending JSON Message: {0}".format(data))
        socket.send_json(data)
        time.sleep(1)


if __name__ == '__main__':
    main()
