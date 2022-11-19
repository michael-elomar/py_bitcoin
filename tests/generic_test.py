import unittest
from termcolor import colored


class Logger:
    @staticmethod
    def _print(tag, msg):
        from datetime import datetime as dt
        timestamp = dt.now()
        print(f"{timestamp} - {tag} - {msg}")

    def info(self, msg):
        tag = colored("[INFO]", "green")
        self._print(tag, msg)

    def debug(self, msg):
        tag = colored("[DEBUG]", "blue")
        self._print(tag, msg)

    def error(self, msg):
        tag = colored("[ERROR]", "red")
        self._print(tag, msg)


class GenericTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GenericTest, self).__init__(*args, **kwargs)
        self.logger = Logger()


