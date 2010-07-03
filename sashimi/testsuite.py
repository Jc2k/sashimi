
import unittest

class TestSuite(unittest.TestSuite):

    def __init__(self, mixin):
        self.mixin = mixin


