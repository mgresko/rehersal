import os
import sys
import logging
import logging.config
import logging.handlers

import yaml


# establish the root directory
root_dir = os.path.abspath(os.path.join(os.path.dirname(
    os.path.abspath(__file__)), ".."))

if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

# set path for config file
config_path = os.path.abspath(os.path.join(root_dir, 'etc', 'config.yaml'))

if not (os.path.exists(config_path) or os.path.islink(config_path)):
    error_msg = "Could not find the config file {}\n\n".format(config_path)
    print >>sys.stderr, error_msg
    sys.exit(1)

# load the config
from bunch import BunchDict
c = BunchDict(yaml.load(open(config_path, "r")))

# configure logging
logging.config.dictConfig(c['logging'])
logging.getLogger(__name__).debug('Logging Configured')
logging.getLogger(__name__).debug('root dir: {}'.format(root_dir))
