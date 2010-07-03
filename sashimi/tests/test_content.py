from unittest import TestCase
from mock import Mock
from sashimi.content import ContentMapVisitor

class TestContent(TestCase):

    def test_empty_content_map(self):
        m = Mock()
        c = ContentMapVisitor(m)
        c.fuzz()
