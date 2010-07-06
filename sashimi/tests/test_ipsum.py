from unittest import TestCase
from sashimi.generators.ipsum import Ipsum, LinesFuzzer, StringFuzzer, TextFuzzer

class TestIpsum(TestCase):

    def test_ipsum(self):
        i = Ipsum()
        self.failUnless(i.get_paragraphs() > 0)

    def test_string_fuzz(self):
        s = TextFuzzer()
        f = s.fuzz({})
        self.failUnless(len(f) > 0)

    def test_text_fuzz(self):
        s = StringFuzzer()
        f = s.fuzz({})
        self.failUnless(len(f) > 0)

    def test_lines_fuzz(self):
        s = LinesFuzzer()
        f = s.fuzz({})
        self.failUnless(len(f) > 0)


