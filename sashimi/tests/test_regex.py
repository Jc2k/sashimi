import unittest
import re

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

    def test_url_regex(self):
        a = get_regex_tree(r'(http|ssh)s?://[^\s\r\n]+')
        self.failUnlessEqual(a.graph(),
            "Sq(Al(Sq(Ch,Ch,Ch,Ch),Sq(Ch,Ch,Ch)),Re(Ch),Ch,Ch,Ch,Re(Cc^(Cc,Ch,Ch)))")


class TestRegexGeneration(unittest.TestCase):

    def test_repetition(self):
        a = get_regex_tree("a?")
        self.failUnless(a.random() in [
            "",
            "a",
            ])

    def test_grouping(self):
        a = get_regex_tree("((foo|bar)|baz)")
        self.failUnless(a.random() in [
            "foo",
            "bar",
            "baz",
            ])

    def test_grouping_then_sequence(self):
        a = get_regex_tree("(foo|bar)baz")
        self.failUnless(a.random() in [
            "foobaz",
            "barbaz",
            ])

    def test_url_regex(self):
        regex = r'(http|ssh)s?://[^\s\r\n]+'
        matcher = re.compile(regex)
        a = get_regex_tree(regex)
        for i in range(50):
            subject = a.random()
            if not matcher.match(subject):
                raise ValueError("'%s' isnt right!" % subject)

