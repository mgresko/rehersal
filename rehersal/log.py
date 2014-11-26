import zmq
from zmq.log.handlers import PUBHandler


class ZMQPUBHandler(PUBHandler):
    """Custom class for zmq pub handler"""

    def __init__(self, sock, root_topic):
        """
        :param string sock: zmq address
        :param string root_topic: prefix for log message topic
        """
        context = zmq.Context()
        publisher = context.socket(zmq.PUB)
        publisher.connect(sock)
        super(ZMQPUBHandler, self).__init__(publisher, context)
        self.root_topic = root_topic
