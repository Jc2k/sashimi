try:
    from Products.LinguaPlone import public as atapi
except ImportError:
    from Products.Archetypes import atapi

from sashimi.node import Node
from sashimi.content_factory import ContentFactory


class ContentTypeRoot(Node):

    info = {
        "fields": {},
    }

    def get_breadcrumb(self):
        return "Site Root"

    def create(self, parent, portal):
        class Dummy(object):
            pass
        dummy = Dummy()
        dummy.content_type = self
        dummy.url = portal.absolute_url()
        dummy.ob = portal
        dummy.data = {}
        dummy.errors = {}
        return dummy

    def create_chain(self, portal):
        return self.create(None, portal)


class ContentType(Node):

    def __init__(self, info):
        super(ContentType, self).__init__()
        self.content_type = info["portal_type"]
        self.info = info

    def get_breadcrumb(self):
        if self.parent:
            return "%s -> %s" % (self.parent.get_breadcrumb(), self.content_type)
        return self.content_type

    def create(self, parent, portal):
        c = ContentFactory(parent, self, portal)
        return c.fuzz()

    def create_chain(self, portal):
        # Visit this chain to its root and build a todo list
        sequence = []
        node = self
        while node:
            sequence.insert(0, node)
            node = node.parent
            #FIXME: HACK
            if isinstance(node, ContentTypeRoot):
                break

        # Starting at the portal, build the thing.
        parent = None
        for node in sequence:
            parent = node.create(parent, portal)
        return parent


class ContentTypeVisitor(object):

    def __init__(self, portal):
        self.portal = portal
        self.visit_list = []
        self.content_types = set()

    def update_metadata(self):
        self.content_types = {}
        for atapi_info in atapi.listTypes():
            at = atapi_info.copy()
            if not at["portal_type"] in self.portal.portal_types:
                continue
            pt = self.portal.portal_types[at["portal_type"]]
            at['allowed_types'] = pt.allowed_content_types
            at["_finishConstruction"] = pt._finishConstruction
            self.content_types[at["portal_type"]] = at

    def visit_types(self):
        root = ContentTypeRoot()

        self.update_metadata()

        ps = self.portal.portal_types[self.portal.portal_type]
        for content_type in ps.allowed_content_types:
             self.visit_type(self.content_types[content_type], root)

        return root

    def visit_type(self, info, parent):
        content_type = info["portal_type"]
        self.visit_list.append(content_type)

        c = ContentType(info)
        parent.append_child(c)

        schema = info["schema"]
        info['fields'] = {}
        for field in schema.fields():
            if field.getName() in ("id", "language"):
                continue
            field_info = self.visit_field(schema[field.getName()])
            info['fields'][field.getName()] = field_info

        for allowed in info["allowed_types"]:
            if not allowed in self.content_types:
                continue
            a = self.content_types[allowed]
            # Don't descend if i'm already in the visit list:
            #  should allow Foo -> Foo, but stop Foo -> Foo -> Foo
            if not allowed in self.visit_list:
                self.visit_type(a, c)

        self.visit_list.remove(content_type)

    def visit_field(self, field):
        info = {}
        info["field"] = field

        info['visible'] = True
        if field.widget.visible == False:
            info['visible'] = False
        elif isinstance(field.widget.visible, dict):
            if "edit" in field.widget.visible:
                info['visible'] = field.widget.visible['edit'] == "visible"

        info['type'] = field.type

        for validator in field.validators:
            if hasattr(validator, "regex"):
                info["regex"] = validator.regex
            if hasattr(validator, "min"):
                info["min"] = validator.min
            if hasattr(validator, "max"):
                info["max"] = validator.max

        # If this field has a list of acceptable values, capture a list of them
        if hasattr(field, "enforceVocabulary") and field.enforceVocabulary:
            info["vocabulary"] = [x for x in field.vocabulary]

        return info

