import os
import random

from sashimi.generators.registry import registry

class Reference(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "reference":
            return True
        return False

    def fuzz(self, field):
        return None

registry.register(Reference)

