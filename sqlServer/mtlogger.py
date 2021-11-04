import logging
import sys
import multiprocessing

class MultithreadedLogger():
    def __init__(self, queue, logging_level):
        self.levels = {
            "debug": logging.DEBUG,
            "info": logging.INFO,
            "warn": logging.WARN,
            "error": logging.ERROR,
            "critical": logging.CRITICAL
        }
        logging.basicConfig(level=self.levels[logging_level], stream=sys.stdout)
        self.queue = queue
        self.logger = logging.getLogger()

        self.logger.info("Logging initialized")
        print("LOGGING LEVEL:", self.levels[logging_level])

    def log(self, type_, msg):
        self.queue.put((type_, msg))

    def logging_mainloop(self):
        # Should be called as a process, goes through the queue and logs it and stuff
        while True:
            try:
                a = self.queue.get()
                if a[0] == "debug":
                    self.logger.debug(a[1])
                elif a[0] == "info":
                    self.logger.info(a[1])
                elif a[0] == "warn":
                    self.logger.warn(a[1])
                elif a[0] == "error":
                    self.logger.error(a[1])
                elif a[0] == "critical":
                    self.logger.critical(a[1])
            except Exception as exc:
                self.logger.error(traceback.format_exc() + " in logging_mainloop")