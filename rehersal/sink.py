import logging

import zmq

from config import c

log = logging.getLogger(__name__)

def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(c.zmq_logging.sub_endpoint)
    subscriber.setsockopt(zmq.SUBSCRIBE, '')

    while True:
        message = subscriber.recv_multipart()
        topic = message[0]
        data = ' '.join(message[1:])
        print "Sink - Message: {}".format(message)
        print "Sink - Topic: {} Data: {}".format(topic, data)

if __name__ == '__main__':
    main()
