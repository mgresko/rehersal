import logging
from multiprocessing import Process

import zmq
from zmq.eventloop import ioloop, zmqstream

from config import c


class ZMQProcess(Process):

    def __init__(self):
        super(ZMQProcess, self).__init__()
        self.context = zmq.Context()
        self.loop = ioloop.IOLoop.instance()

    def setup(self):
        pass

    def stream(self, sock_type, conn_str, bind, callback=None, subscribe=b''):
        sock = self.context.socket(sock_type)

        if bind:
            sock.bind(conn_str)
        else:
            sock.connect(conn_str)

        if sock_type == zmq.SUB:
            sock.setsockopt(zmq.SUBSCRIBE, subscribe)

        stream = zmqstream.ZMQStream(sock, self.loop)
        if callback:
            stream.on_recv(callback)

        return stream
