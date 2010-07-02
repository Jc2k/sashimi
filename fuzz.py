
import weakref

from AccessControl.SecurityManagement import newSecurityManager
from Testing.makerequest import makerequest

import transaction

def login(app, manager_user):
    user = app.acl_users.getUserById(manager_user).__of__(app.acl_users)
    newSecurityManager(None, user)
    return makerequest(app)

class Node(object):

    def __init__(self):
        self.parent = None
        self.children = []

    def set_parent(self, parent):
        self.parent = weakref.ref(parent)

    def append_child(self, child):
        self.children.append(child)
        child.set_parent(self)

    def visit(self, visitor):
        visitor.visit_node(self)
        for child in self.children:
            child.visit(visitor)


class ContentTypeRoot(Node):

    def get_breadcrumb(self):
        return "Site Root"


class ContentType(Node):

    def __init__(self, content_type, info):
        super(ContentType, self).__init__()
        self.content_type = content_type
        self.info = info

    def get_breadcrumb(self):
        if self.parent():
            return "%s -> %s" % (self.parent().get_breadcrumb(), self.content_type)
        return self.content_type


class Content(Node):

    def __init__(self, content_type):
        self.content_type = content_type

    def fuzz(self):
        info = self.content_type.info

        app.portal.portal_types.constructContent(self.content_type.content_type, app.portal, "fred", None)
        ob = app.portal.get("fred")

        print self.content_type.get_breadcrumb()
        for key in ob.schema.keys():
            field = ob.schema[key]

            if field.widget.visible == False:
                continue

            if isinstance(field.widget.visible, dict):
                if "edit" in field.widget.visible:
                    if field.widget.visible["edit"] == "invisible":
                        continue

            # THIS IS WHERE WE GENERATE SOME DUMMY CONTENT FOR THAT KIND OF FIELD
            # WE NEED TO FUZZ FOR:
            # set(['string', 'reference', 'text', 'image', 'lines', 'datetime', 'boolean', 'file'])

        info._finishConstruction(ob)

        transaction.abort()

class ContentTypeVisitor(object):

    def __init__(self, portal):
        self.portal = portal
        self.visit_list = []

    def visit_types(self):
        root = ContentTypeRoot()

        content_types = frozenset(self.portal.portal_types.listContentTypes())
        marked_content_types = set()
        for content_type in content_types:
            info = self.portal.portal_types[content_type]
            marked_content_types.update(info.allowed_content_types)

        root_content_types = content_types - marked_content_types
        for content_type in root_content_types:
            info = self.portal.portal_types[content_type]
            self.visit_type(content_type, info, root)

        return root

    def visit_type(self, content_type, info, parent):
        self.visit_list.append(content_type)

        for allowed in info.allowed_content_types:
            a = self.portal.portal_types[allowed]
            c = ContentType(allowed, a)
            parent.append_child(c)

            # Don't descend if i'm already in the visit list: should allow Foo -> Foo, but stop Foo -> Foo -> Foo
            if not allowed in self.visit_list:
                self.visit_type(allowed, a, c)

        self.visit_list.remove(content_type)


class ContentMapVisitor(object):

    def __init__(self, map):
        self.map = map

    def visit_node(self, node):
        if not isinstance(node, ContentType):
            return
        c = Content(node)
        c.fuzz()

    def fuzz(self):
        self.map.visit(self)

app = login(app, "zopeadmin")

a = ContentTypeVisitor(app.portal)
map = a.visit_types()

b = ContentMapVisitor(map)
b.fuzz()

