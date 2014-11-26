import logging
from multiprocessing import Process

import zmq
from zmq.eventloop import ioloop, zmqstream

from config import c
from base import ZMQProcess
from handler import AgentStreamHandler
from puppet import Puppet
from utils import import_from_string


log = logging.getLogger(__name__)


class Agent(ZMQProcess):

    def __init__(self, conn_str, subscribe, puppet_handler):
        super(Agent, self).__init__()
        self.conn_str = conn_str
        self.sub_stream = None
        self.puppet_handler = puppet_handler
        self.subscribe = subscribe

    def __str__(self):
        return 'Agent {0}'.format(self.__dict__)

    def setup(self):
        # setup the puppet handler
        self.sub_stream = self.stream(zmq.SUB, self.conn_str, bind=False,
                                         subscribe=self.subscribe)
        self.sub_stream.on_recv(AgentStreamHandler(
                                    self.sub_stream, self.stop,
                                    self.puppet_handler))

    def run(self):
        self.setup()
        self.loop.start()

    def stop(self):
        self.loop.stop()

if __name__ == '__main__':
    # setup the repo
    scm = import_from_string(c.scm.klass)
    repo = scm(c.scm.repo_url)
    log.info('Initializing scm: {0}'.format(repo.repo_url))

    # initialize puppet handler
    puppet_handler = Puppet(
        module_path=c.puppet.module_path,
        manifest_path=c.puppet.manifest_path,
        scm=repo,
        nice=c.puppet.nice)
    log.info('Puppet Handler initialized: {0}'.format(puppet_handler))

    # intialize the Agent
    agent = Agent(
        conn_str=c.broker.pub_endpoint,
        subscribe=c.agent.topic,
        puppet_handler=puppet_handler)
    log.info('Agent initialized: {0}'.format(agent))

    # start the Agent
    log.info("Agent Starting")
    agent.run()
