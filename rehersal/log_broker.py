import logging
import traceback
from multiprocessing import Process

import zmq

from utils import uninterruptible
from config import c

log = logging.getLogger(__name__)

class LogBroker(Process):

    def run(self):
        """Initializeds the log broker"""
        try:
            context = zmq.Context(1)

            # setup log broker
            log_sub = context.socket(zmq.SUB)
            log_sub.bind(c.zmq_logging.sub_bind)
            log_sub.setsockopt(
                zmq.SUBSCRIBE, "{0}".format(c.logging.handlers.zmq.root_topic)
            )

            log_pub = context.socket(zmq.PUB)
            log_pub.bind(c.zmq_logging.pub_bind)

            print "starting zmq logging broker"
            uninterruptible(zmq.device, zmq.FORWARDER, log_sub, log_pub)
        except KeyboardInterrupt:
            print "Killing, keyboard interrupt"
        except Exception:
            traceback.print_exc()
            print "bringing down applicaiotn zmq broker"
        finally:
            log_sub.close()
            log_pub.close()
            context.term()

if __name__ == '__main__':
    log_broker = LogBroker()
    log_broker.run()
