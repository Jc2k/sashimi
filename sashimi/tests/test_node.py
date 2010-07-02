from unittest import TestCase
from sashimi.node import Node

class TestNode(TestCase):

    def test_root(self):
        node = Node()
        self.failUnlessEqual(node.parent, None)
        self.failUnlessEqual(len(node.children), 0)

    def test_chain(self):
        parent = Node()
        child = Node()
        parent.append_child(child)
        self.failUnlessEqual(child.parent, parent)
        self.failUnless(child in parent.children)
