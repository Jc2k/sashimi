from unittest import TestCase
from sashimi.generators.ipsum import Ipsum, UpsideDownIpsum

class TestIpsum(TestCase):

    def test_ipsum(self):
        i = Ipsum()
        i.fuzz({})

    def test_udipsum(self):
        i = UpsideDownIpsum()
        i.fuzz({})

