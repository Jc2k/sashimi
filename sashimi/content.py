import transaction
import uuid

from sashimi.node import Node
from sashimi.contenttypes import ContentType
from sashimi.generators.registry import registry

class Content(Node):

    def __init__(self, parent, content_type, portal):
        self.parent_node = parent
        self.content_type = content_type
        self.portal = portal

        self.id = str(uuid.uuid4())
        self.ob = None
        self.data = {}
        self.url = None
        self.errors = {}

    def fuzz_field(self, field_info, field):
        for fuzzer in registry.get_fuzzers(field_info):
            data = fuzzer.fuzz(field_info)
            mutator = field.getMutator(self.ob)
            if mutator:
                mutator(data)
                return data
        return None

    def fuzz(self):
        info = self.content_type.info

        if self.parent_node:
            parent = self.parent_node.ob
        else:
            parent = self.portal

        try:
            self.portal.portal_types.constructContent(self.content_type.content_type, parent, self.id, None)
        except:
            #AccessControl_Unauthorized ?
            return
        self.ob = parent.get(self.id)

        if "schema" not in dir(self.ob):
            return

        print self.content_type.get_breadcrumb()

        for field, info in self.content_type.info["fields"].iteritems():
            if not info['visible']:
                continue

            data = self.fuzz_field(info, info["field"])
            if data:
                self.data[field] = data

        self.ob.Schema().validate(self.ob, None, self.errors, True, True)
        assert len(self.errors.keys()) == 0

        self.content_type.info["_finishConstruction"](self.ob)
        transaction.commit()

        self.url = self.ob.absolute_url()


class ContentMapVisitor(object):

    def __init__(self, map):
        self.map = map
        self.content_types = []

    def enter_node(self, node):
        self.content_type.append(node)

    def __iter__(self):
        self.map.visit(self)
        return iter(self.content_types)


def fuzz_content_types(map, portal, report):
    visitor = ContentMapVisitor(map)
    urls = []
    for content_type in map:
        try:
            #FIXME: First portal is parent node
            c = Content(portal, content_type, portal)
            c.fuzz()
            urls.append((c.url, c))
        except:
            report.exception(c)
        else:
            report.success(c)

    return urls

