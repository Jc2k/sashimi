import transaction
import uuid

from sashimi.generators.registry import registry

class ContentFactory(object):

    def __init__(self, parent, content_type, portal):
        self.parent_node = parent
        self.content_type = content_type
        self.portal = portal

        self.id = str(uuid.uuid4())
        self.errors = {}

    def fuzz_field(self, field_info, field, ob):
        for fuzzer in registry.get_fuzzers(field_info):
            data = fuzzer.fuzz(field_info)
            mutator = field.getMutator(ob)
            if mutator:
                mutator(data)
                return data
        return None

    def fuzz_fields(self, content_type, ob):
        data = {}

        for field, info in content_type.info["fields"].iteritems():
            if not info['visible']:
                continue

            field_data = self.fuzz_field(info, info["field"], ob)
            if field_data:
                data[field] = field_data

        return data

    def fuzz(self):
        errors = {}
        data = {}
        info = self.content_type.info

        if self.parent_node:
            parent = self.parent_node.ob
        else:
            parent = self.portal

        print self.content_type.get_breadcrumb()

        try:
            self.portal.portal_types.constructContent(self.content_type.content_type, parent, self.id, None)
        except:
            #AccessControl_Unauthorized ?
            return
        ob = parent.get(self.id)

        if "schema" not in dir(ob):
            return

        try:
            data = self.fuzz_fields(self.content_type, ob)
            ob.Schema().validate(ob, None, errors, True, True)
            self.content_type.info["_finishConstruction"](ob)
            transaction.commit()
        finally:
            return Content(ob, ob.absolute_url(), self.content_type, data, errors)


class Content(object):

    def __init__(self, ob, url, content_type, data, errors):
        self.ob = ob
        self.url = url
        self.content_type = content_type
        self.data = data
        self.errors = errors

    def browse(self, browser):
        # For now, just hit our main URL
        # TODO: Hit forms and pagination links
        browser.open(self.url)

