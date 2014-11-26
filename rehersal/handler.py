import logging

from zmq.utils import jsonapi as json

from config import c

log = logging.getLogger(__name__)


class MessageHandler(object):

    def __init__(self, json_load=-1):
        self._json_load = json_load

    def __call__(self, msg):
        i = self._json_load
        msg_type, data = json.loads(msg[i])
        msg[i] = data

        if msg_type.startswith('_'):
            raise AttributeError('{0} starts with an "_"'.format(msg_type))

        getattr(self, msg_type)(*msg)


class AgentStreamHandler(MessageHandler):

    def __init__(self, sub_stream, stop, request_handler):
        super(AgentStreamHandler, self).__init__()
        self._sub_stream = sub_stream
        self._stop = stop
        self._request_handler = request_handler

    def puppet(self, data):
        """Run puppet with given branch"""
        log.info("Running puppet on branch: {0}".format(data['branch']))
