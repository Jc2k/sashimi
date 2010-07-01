
import weakref

class Node(object):

    """
    I am a node in a DAG

    I retain a strong pointer to my parent object

    I have a weak list of my children
    """

    def __init__(self):
        self.parent = None
        self.children = weakref.WeakValueDictionary()

    def set_parent(self, parent):
        self.parent = parent

    def append_child(self, child):
        self.children[id(child)] = child
        child.set_parent(self)

    def visit(self, visitor):
        visitor.visit_node(self)
        for child in self.children.iteritems():
            child.visit(visitor)


class ContentType(Node):

    def __init__(self, content_type, info):
        super(ContentType, self).__init__()
        self.content_type = content_type
        self.info = info

    def get_breadcrumb(self):
        if self.parent:
            return "%s -> %s" % (self.parent.get_breadcrumb(), self.content_type)
        return self.content_type


class Analyzer(object):

    def __init__(self, portal):
        self.portal = portal
        self.visit_list = []

    def visit_types(self):
        root = ContentType("/", None)

        content_types = frozenset(self.portal.portal_types.listContentTypes())
        marked_content_types = set()
        for content_type in content_types:
            info = self.portal.portal_types[content_type]
            marked_content_types.update(info.allowed_content_types)

        root_content_types = content_types - marked_content_types
        for content_type in root_content_types:
            info = self.portal.portal_types[content_type]
            self.visit_type(content_type, info, root)

    def visit_type(self, content_type, info, parent):
        self.visit_list.append(content_type)

        for allowed in info.allowed_content_types:
            a = self.portal.portal_types[allowed]
            c = ContentType(allowed, a)
            parent.append_child(c)
            print c.get_breadcrumb()

            # Don't descend if i'm already in the visit list: should allow Foo -> Foo, but stop Foo -> Foo -> Foo
            if not allowed in self.visit_list:
                self.visit_type(allowed, a, c)

        self.visit_list.remove(content_type)

a = Analyzer(app.portal)
a.visit_types()
