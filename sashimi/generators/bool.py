
import random
from sashimi.generators.registry import registry

class Bool(object):

    @classmethod
    def can_fuzz(cls, field):
        if field["type"] == "boolean":
            return True
        return False

    def fuzz(self, field):
        return random.choice((True, False))

registry.register(Bool)

