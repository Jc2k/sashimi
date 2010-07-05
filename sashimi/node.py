import weakref


class Node(object):

    name = "Node"

    def __init__(self):
        self._parent = None
        self.children = []

    def set_parent(self, parent):
        self._parent = weakref.ref(parent)

    def get_parent(self):
        if self._parent:
            return self._parent()

    parent = property(get_parent, set_parent)

    def append_child(self, child):
        self.children.append(child)
        child.set_parent(self)

    def reparent_child(self, child, new_parent):
        self.children.remove(child)
        new_parent.append_child(child)

    def graph(self):
        if self.children:
            return "%s(%s)" % (self.name, ",".join(x.graph() for x in self.children))
        return self.name

    def visit(self, visitor):
        visitor.enter_node(self)
        for child in self.children:
            child.visit(visitor)
        visitor.leave_node(self)
