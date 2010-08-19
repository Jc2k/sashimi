import os
import random

from sashimi.generators.registry import registry

class Reference(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "reference":
            return True
        return False

    def fuzz(self, field, content_types):
        for pt, ct in content_types.portal.objectItems():
            if ct.portal_type in content_types.chains:
                return ct.UID()

registry.register(Reference)

