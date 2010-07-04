import transaction

from sashimi.node import Node
from sashimi.contenttypes import ContentType

class Content(Node):

    def __init__(self, content_type, portal):
        self.content_type = content_type
        self.portal = portal

    def fuzz(self):
        info = self.content_type.info

        self.portal.portal_types.constructContent(self.content_type.content_type, self.portal, "fred", None)
        ob = self.portal.get("fred")

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


class ContentMapVisitor(object):

    def __init__(self, map, portal):
        self.map = map
        self.portal = portal

    def visit_node(self, node):
        if not isinstance(node, ContentType):
            return
        c = Content(node, self.portal)
        c.fuzz()

    def fuzz(self):
        self.map.visit(self)


