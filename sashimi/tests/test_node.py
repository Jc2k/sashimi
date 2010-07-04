from unittest import TestCase
from mock import Mock
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

    def test_visit(self):
        visitor = Mock()
        parent = Node()
        child = Node()
        parent.append_child(child)
        parent.visit(visitor)
        self.failUnlessEqual(visitor.enter_node.call_count, 2)
        self.failUnlessEqual(visitor.leave_node.call_count, 2)

