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
        self.url = None

    def get_field_info(self, field):
        info = {}

        info['visible'] = True
        if field.widget.visible == False:
            info['visible'] = False
        elif isinstance(field.widget.visible, dict):
            if "edit" in field.widget.visible:
                info['visible'] = field.widget.visible['edit'] == "visible"

        info['type'] = field.type

        return info

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
        for key in self.ob.schema.keys():
            field = self.ob.schema[key]
            field_info = self.get_field_info(field)

            if not field_info['visible']:
                continue

            for fuzzer in registry.get_fuzzers(field_info):
                data = fuzzer.fuzz(field_info)
                field.getMutator()(data)
                break
            else:
                #print "Couldn't fuzz any data for %s (%s)" % (key, field_info)
                pass

        info._finishConstruction(self.ob)
        transaction.commit()

        self.url = self.ob.absolute_url()


class ContentMapVisitor(object):

    def __init__(self, map, portal):
        self.map = map
        self.portal = portal
        self.stack = []
        self.urls = []

    def enter_node(self, node):
        if not isinstance(node, ContentType):
            return

        parent = None
        if self.stack:
            parent = self.stack[0]

        c = Content(parent, node, self.portal)
        c.fuzz()
        self.urls.append((c.url, c))

        self.stack.insert(0, c)

    def leave_node(self, node):
        if not isinstance(node, ContentType):
            return

        assert node == self.stack[0].content_type
        self.stack.pop(0)

    def fuzz(self):
        self.map.visit(self)
        return self.urls

