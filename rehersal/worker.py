import logging

import zmq

from config import c

log = logging.getLogger(__name__)


def main():
    context = zmq.Context()
    subscriber = context.socket(zmq.SUB)
    subscriber.connect(c.broker.pub_endpoint)
    subscriber.setsockopt(zmq.SUBSCRIBE, c.agent.topic)

    publisher = context.socket(zmq.PUB)
    publisher.connect(c.broker.sub_endpoint)

    while True:
        message = subscriber.recv_multipart()
        topic = message[0]
        data = ' '.join(message[1:])
        print "Received request: %s" % message
        log.info('{}_ENDD'.format(data))
        print "Topic: " + topic + " MessageData: " + data
        publisher.send('complete finished_{0}'.format(data))

if __name__ == '__main__':
    main()
