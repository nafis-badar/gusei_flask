import logging
import sys
from com.gusei.DefinePaths.DefinePaths import DefinePath
# from com.gusei.altranUtils.utility import Utility
from com.gusei.utils.utils import Utils
from logging.handlers import TimedRotatingFileHandler
logFilePath = DefinePath.getLogFilePath()
logger = logging.getLogger('')
logger.setLevel(logging.ERROR)
# fh = TimedRotatingFileHandler(logFilePath + 'log_'+str(Utils.get_static_ist_time(),when="midnight", interval=1)
sh = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] - %(funcName)s - %(message)s',
                               datefmt='%a, %d %b %Y %H:%M:%S')
# fh.setFormatter(formatter)
sh.setFormatter(formatter)
# logger.addHandler(fh)
logger.addHandler(sh)


import logging

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

# Creating an object
logger = logging.getLogger()

def get_logger():
    return logger
