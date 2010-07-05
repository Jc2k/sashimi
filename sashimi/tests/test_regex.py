import unittest
import mock

from sashimi.generators.regex import get_regex_tree

class TestReqex(unittest.TestCase):

    def test_repetition(self):
        a = get_regex_tree("a+")
        self.failUnlessEqual(a.graph(), "Sq(Re(Ch))")

    def test_characters(self):
        a = get_regex_tree("foo")
        self.failUnlessEqual(a.graph(), "Sq(Ch,Ch,Ch)")

    def test_grouping(self):
        a = get_regex_tree("(foo|bar)")
        self.failUnlessEqual(a.graph(), "Sq(Al(Sq(Ch,Ch,Ch),Sq(Ch,Ch,Ch)))")

    def test_grouping_repetition(self):
        a = get_regex_tree("(foo|bar){1,2}")
        self.failUnlessEqual(a.graph(), "Sq(Re(Al(Sq(Ch,Ch,Ch),Sq(Ch,Ch,Ch))))")

    def test_multiple_grouping(self):
        a = get_regex_tree("(f|o|o|b|a|r)")
        self.failUnlessEqual(a.graph(), "Sq(Al(Sq(Ch),Sq(Ch),Sq(Ch),Sq(Ch),Sq(Ch),Sq(Ch)))")

    def test_nested_grouping(self):
        a = get_regex_tree("((foo|bar)|baz)")
        self.failUnlessEqual(a.graph(), "Sq(Al(Sq(Al(Sq(Ch,Ch,Ch),Sq(Ch,Ch,Ch))),Sq(Ch,Ch,Ch)))")
