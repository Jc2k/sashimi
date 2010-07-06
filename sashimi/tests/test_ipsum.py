from unittest import TestCase
from sashimi.generators.ipsum import Ipsum

class TestIpsum(TestCase):

    def test_ipsum(self):
        i = Ipsum()
        self.failUnless(i.get_paragraphs() > 0)
