import errno

import zmq

def uninterruptible(f, *args, **kwargs):
    """Function for wrapping zmq device"""
    while True:
        try:
            return f(*args, **kwargs)
        except zmq.ZMQError as e:
            if e.errno == errno.EINTR:
                continue
            else:
                raise


def import_from_string(name):
    """importer for class from string"""
    components = name.split('.')
    mod_path = '.'.join(components[:1])
    klass = components[-1:][0]
    mod = __import__(mod_path)
    mod = getattr(mod, klass)
    return mod
