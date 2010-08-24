import os
import random

from Products.CMFCore.utils import getToolByName

from sashimi.generators.registry import registry

class Reference(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "reference":
            return True
        return False

    def fuzz(self, field, content_types):
        if field["allowed_types"]:
            # Pick a random allowed_type
            pt = random.choice(field["allowed_types"])

            # Do we have one already?
            pc = getToolByName(content_types.portal, 'portal_catalog')
            results = pc({"portal_type": pt})
            if results:
                return random.choice(results).UID

            # We dont have one, create one
            ct = random.choice(content_types.chains[pt])
            new_obj = ct.create_chain(content_types.portal, lazy=True)
            return new_obj.ob.UID()

        for pt, ct in content_types.portal.objectItems():
            if ct.portal_type in content_types.chains:
                return ct.UID()

registry.register(Reference)

