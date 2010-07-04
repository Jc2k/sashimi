import transaction
import uuid

from sashimi.node import Node
from sashimi.contenttypes import ContentType

class Content(Node):

    def __init__(self, parent, content_type, portal):
        self.parent_node = parent
        self.content_type = content_type
        self.portal = portal

        self.id = str(uuid.uuid4())
        self.ob = None

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

        self.portal.portal_types.constructContent(self.content_type.content_type, parent, self.id, None)
        self.ob = parent.get(self.id)

        print self.content_type.get_breadcrumb()
        for key in self.ob.schema.keys():
            field = self.ob.schema[key]
            field_info = self.get_field_info(field)

            if not field_info['visible']:
                continue

            # THIS IS WHERE WE GENERATE SOME DUMMY CONTENT FOR THAT KIND OF FIELD
            # WE NEED TO FUZZ FOR:
            # set(['string', 'reference', 'text', 'image', 'lines', 'datetime', 'boolean', 'file'])

        info._finishConstruction(self.ob)

        transaction.commit()


class ContentMapVisitor(object):

    def __init__(self, map, portal):
        self.map = map
        self.portal = portal
        self.stack = []

    def enter_node(self, node):
        if not isinstance(node, ContentType):
            return

        parent = None
        if self.stack:
            parent = self.stack[0]

        c = Content(parent, node, self.portal)
        c.fuzz()
        self.stack.insert(0, c)

    def leave_node(self, node):
        assert node == self.stack[0].content_type
        self.stack.pop(0)

    def fuzz(self):
        self.map.visit(self)


