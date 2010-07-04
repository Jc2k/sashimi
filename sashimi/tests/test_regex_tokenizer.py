from unittest import TestCase
from mock import Mock

from sashimi.generators.regex import Tokenizer


class TestRegexTokenizer(TestCase):

    def setUp(self):
        self.visitor = Mock()
        self.t = Tokenizer()

    def test_character(self):
        self.t.visit("apple", self.visitor)
        self.failUnlessEqual(self.visitor.character.call_count, 5)

    def test_grouping(self):
        self.t.visit("^(fred|george)", self.visitor)
        self.failUnlessEqual(self.visitor.start_group.call_count, 1)
        self.failUnlessEqual(self.visitor.end_group.call_count, 1)

    def test_precise_repetition(self):
        self.t.visit("fred{2,999}", self.visitor)
        self.failUnlessEqual(self.visitor.repetition.call_args, ((2, 999), {}))


