import sys
import transaction
import uuid

from Products.Archetypes.event import ObjectInitializedEvent
from zope import event

from sashimi.generators.registry import registry

class ContentFactory(object):

    def __init__(self, parent, content_type, portal, content_types):
        self.parent_node = parent
        self.content_type = content_type
        self.portal = portal
        self.content_types = content_types

        self.id = str(uuid.uuid4())
        self.errors = {}

    def fuzz_field(self, field_info, field, ob):
        for fuzzer in registry.get_fuzzers(field_info):
            data = fuzzer.fuzz(field_info, self.content_types)
            mutator = field.getMutator(ob)
            if mutator:
                mutator(data)
                return data
        return None

    def fuzz_fields(self, c):
        for field, info in c.content_type.info["fields"].iteritems():
            if not info['visible']:
                continue

            field_data = self.fuzz_field(info, info["field"], c.ob)
            if field_data:
                c.data[field] = field_data

    def fuzz(self):
        errors = {}
        data = {}
        info = self.content_type.info

        if self.parent_node:
            parent = self.parent_node.ob
        else:
            parent = self.portal

        print self.content_type.get_breadcrumb()

        parent.invokeFactory(self.content_type.content_type, self.id)
        ob = parent.get(self.id)

        if "schema" not in dir(ob):
            return

        c = Content(ob, self.content_type)

        try:
            self.fuzz_fields(c)
            ob.Schema().validate(ob, None, c.errors, True, True)

            # Because this is a programmatic object creation, certain things dont happen
            # that we want to. Short term we can just force them, long term we probably
            # need to do POST's to create our objects?
            event.notify(ObjectInitializedEvent(ob))
            ob.at_post_create_script()

            transaction.commit()
        except:
            c.traceback = sys.exc_info()

        c.url = ob.absolute_url()
        return c


class Content(object):

    def __init__(self, ob, content_type):
        self.ob = ob
        self.content_type = content_type

        self.url = None
        self.data = {}
        self.errors = {}
        self.traceback = None

    def browse(self, browser):
        # For now, just hit our main URL
        # TODO: Hit forms and pagination links
        browser.open(self.url)

