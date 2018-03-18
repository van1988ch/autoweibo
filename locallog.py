import logging

import sys, logging
from wsgilog import WsgiLog,LogStdout
import config

class Log(WsgiLog):
    def __init__(self, application):
        WsgiLog.__init__(
            self,
            application,
            logformat = config.logformat,
            datefmt = config.datefmt,
            tofile = True,
            file = config.file,
            interval = config.interval,
            backups = config.backups
            )
        sys.stdout = LogStdout(self.logger, logging.INFO)
        sys.stderr = LogStdout(self.logger, logging.ERROR)