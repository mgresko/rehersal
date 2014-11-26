import logging
import traceback
import errno
import signal
from multiprocessing import Process

import zmq

from config import c
from daemon import Daemon


log = logging.getLogger(__name__)


def uninterruptible(f, *args, **kwargs):
    while True:
        try:
            return f(*args, **kwargs)
        except zmq.ZMQError as e:
            if e.errno == errno.EINTR:
                continue
            else:
                raise


class Broker(Daemon):

    def __init__(self, *args, **kwargs):
        super(Broker, self).__init__(*args, **kwargs)
        self._logging_broker_proc = None
        self._app_broker_proc = None

        # register signal handler and make sure the brokers are stopped
        signal.signal(signal.SIGTERM|signal.SIGHUP, self._signal_handler)

    def logging_broker(self):
        try:
            context = zmq.Context(1)
            log_sub = context.socket(zmq.SUB)
            log_sub.bind(c.zmq_logging.sub_bind)
            log_sub.setsockopt(
                zmq.SUBSCRIBE, "{0}".format(c.logging.handlers.zmq.root_topic)
            )

            log_pub = context.socket(zmq.PUB)
            log_pub.bind(c.zmq_logging.pub_bind)

            print "Starting zmq logging broker"
            uninterruptible(zmq.device, zmq.FORWARDER, log_sub, log_pub)
        except KeyboardInterrupt:
            print "Keyboard Interrupt"
        except Exception, e:
            traceback.print_exc()
            print "bringing down logging zmq device"
        finally:
            log_sub.close()
            log_pub.close()
            context.term()

    def app_broker(self):
        try:
            context = zmq.Context()
            # setup application broker
            subscriber = context.socket(zmq.SUB)
            subscriber.bind(c.broker.sub_bind)
            subscriber.setsockopt(zmq.SUBSCRIBE, "")

            publisher = context.socket(zmq.PUB)
            publisher.bind(c.broker.pub_bind)

            print "Starting zmq application broker"
            uninterruptible(zmq.device, zmq.FORWARDER, subscriber, publisher)
        except KeyboardInterrupt:
            print "Keyboard Interrupt"
        except Exception, e:
            traceback.print_exc()
            print "bringing down application zmq device"
        finally:
            subscriber.close()
            publisher.close()
            context.term()

    def run(self):
        # if enabled, start the zmq logging broker
        if c.zmq_logging.enabled:
            self._logging_broker_proc = Process(target=self.logging_broker).start()

        # start app broker
        self._app_broker_proc = Process(target=self.app_broker).start()

    def broker_stop(self):
        if self._logging_broker_proc:
            print "stopping logging broker"
            self._logging_broker_proc.terminate()

        if self._app_broker_proc.is_alive():
            print "stopping app broker"
            print "self._app_broker_proc"
            self._app_broker_proc.terminate()

    def _signal_handler(self, signal, frame):
        self.broker_stop()
        self.stop()

if __name__ == '__main__':
    broker = Broker('/tmp/broker.pid')
    broker.run()
