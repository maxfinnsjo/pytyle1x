import time, os, sys
from PyTyle.Config import Config
from PyTyle.State import State


class Debug:
    def __init__(self, filename):
        self._log = sys.stderr
        if Config.DEBUG:
            self._log = open(filename, 'a+')
            self.write('\n---------------------------------\nPyTyle started')

    def write(self, msg):
        if not self._log:
            return

        t = time.localtime()
        write = '%d/%d/%d at %d:%d:%d:    %s' % (
            t.tm_mon,
            t.tm_mday,
            t.tm_year,
            t.tm_hour,
            t.tm_min,
            t.tm_sec,
            msg
        )
        print(write, file = self._log)
        self._log.flush()


DEBUG = Debug(os.getenv('HOME') + '/pytyle.log')
