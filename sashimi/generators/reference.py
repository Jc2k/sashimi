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
        return content_types.portal

registry.register(Reference)

